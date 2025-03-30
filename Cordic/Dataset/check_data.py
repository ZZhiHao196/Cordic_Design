import sys
import argparse
from pathlib import Path
from typing import List, Dict, Tuple

class DataValidator:
    def __init__(self, model_dir: Path, rtl_dir: Path):
        self.model_dir = model_dir
        self.rtl_dir = rtl_dir
        self.file_pairs = [
            ("Model_Sin_Out_S0I1F16.dat", "RTL_Sin_Out_S0I1F16.dat"),
            ("Model_Cos_Out_S0I1F16.dat", "RTL_Cos_Out_S0I1F16.dat")
        ]
        self.summary = {
            "total_files": 0,
            "passed_files": 0,
            "error_details": [],
            "max_errors": {"sin": 0, "cos": 0},
            "avg_errors": {"sin": 0.0, "cos": 0.0}
        }

    def validate_all(self, threshold: int = 3) -> bool:
        """Test all the data files"""
        results = []
        for model_file, rtl_file in self.file_pairs:
            model_path = self.model_dir / model_file
            rtl_path = self.rtl_dir / rtl_file
            
            if not self._check_file_exists(model_path, rtl_path):
                continue
                
            errors = self._compare_files(model_path, rtl_path, threshold)
            channel = "sin" if "Sin" in model_file else "cos"
            self._update_summary(channel, errors)
            results.append(len(errors) == 0)

        return all(results)

    def _check_file_exists(self, *paths: Path) -> bool:
        """check all the files exist"""
        for path in paths:
            if not path.exists():
                print(f"[Error] files does not exist: {path}")
                return False
        return True

    def _compare_files(self, model_path: Path, 
                      rtl_path: Path, 
                      threshold: int) -> List[Tuple[int, str, str, int]]:
        """compare single files"""
        model_data = self._read_hex_file(model_path)
        rtl_data = self._read_hex_file(rtl_path)
        
        if len(model_data) != len(rtl_data):
            print(f"[warning] data length not match: {model_path.name} vs {rtl_path.name}")
            return []

        errors = []
        for idx, (m, r) in enumerate(zip(model_data, rtl_data)):
            try:
                m_val = int(m, 16)
                r_val = int(r, 16)
            except ValueError:
                print(f"[format error] {model_path.name} line {idx+1}: {m} vs {r}")
                continue

            if (delta := abs(m_val - r_val)) > threshold:
                errors.append((
                    idx + 1,
                    f"0x{m:>04x}",
                    f"0x{r:>04x}",
                    delta
                ))
        return errors

    def _read_hex_file(self, path: Path) -> List[str]:
        """reading hex file"""
        with open(path, 'r') as f:
            return [line.strip().lower().lstrip('0x') for line in f if line.strip()]

    def _update_summary(self, channel: str, errors: list):
        """updata summary"""
        self.summary["total_files"] += 1
        if not errors:
            self.summary["passed_files"] += 1
            return

        error_count = len(errors)
        max_error = max(errors, key=lambda x: x[3])[3] if errors else 0
        avg_error = sum(e[3] for e in errors) / error_count if errors else 0
        
        self.summary["error_details"].extend(errors)
        self.summary["max_errors"][channel] = max(
            self.summary["max_errors"][channel], max_error
        )
        self.summary["avg_errors"][channel] = (
            self.summary["avg_errors"][channel] * (self.summary["total_files"] - 1) + avg_error
        ) / self.summary["total_files"]

    def generate_report(self):
        """generate report"""
        print("\n" + "="*60)
        print(" CORDIC Validation Report ")
        print(f" Model Data Directory: {self.model_dir}")
        print(f" RTL Data Directory : {self.rtl_dir}")
        print("-"*60)
        print(f" Total Files: {self.summary['total_files']}")
        print(f" Passed Files: {self.summary['passed_files']}")
        print(f" Failed Files: {self.summary['total_files'] - self.summary['passed_files']}")
        print("\n Channel Error Statistics:")
        print(f" SIN Max Error: {self.summary['max_errors']['sin']} LSB")
        print(f" COS Max Error: {self.summary['max_errors']['cos']} LSB")
        print(f" SIN Avg Error: {self.summary['avg_errors']['sin']:.2f} LSB")
        print(f" COS Avg Error: {self.summary['avg_errors']['cos']:.2f} LSB")
        
        if self.summary["error_details"]:
            print("\n Error Examples:")
            for idx, error in enumerate(self.summary["error_details"][:5]):
                print(f" {idx+1}. Line {error[0]:04d} | Model: {error[1]} | RTL: {error[2]} | Δ={error[3]}LSB")
        
        print("="*60)
        print("Validation Result: ", end="")
        if self.summary["passed_files"] == self.summary["total_files"]:
            print("✅ All Passed")
        else:
            print("❌ Exist Errors")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CORDIC Data Validation Tool")
    parser.add_argument("model_dir", help="Model Data Directory Path")
    parser.add_argument("rtl_dir", help="RTL Data Directory Path")
    parser.add_argument("-t", "--threshold", type=int, default=3,
                      help="Allowed Maximum LSB Error (default: 3)")
    
    args = parser.parse_args()
    
    validator = DataValidator(Path(args.model_dir), Path(args.rtl_dir))
    success = validator.validate_all(args.threshold)
    validator.generate_report()
    
    sys.exit(0 if success else 1)