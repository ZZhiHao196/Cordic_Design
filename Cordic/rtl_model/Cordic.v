
module Cordic(
    input wire [16:0] theta,   // 0~pi/2,  Q1.16
    output wire [16:0] sin_out, //Q1.16
    output wire [16:0] cos_out
);


localparam signed [16:0] K =17'sh09B75;  // 1/1.64676 17'h1A592;         

//Q1.16
reg signed [16:0] angles [0:16];    //arctan(2^-i)
integer iter;
initial begin
    angles[0]  = 17'h0C910;
    angles[1]  = 17'h076B2;
    angles[2]  = 17'h03EB7;
    angles[3]  = 17'h01FD6;// i=0~3
    angles[4]  = 17'h00FFB;
    angles[5]  = 17'h007FF;
    angles[6]  = 17'h00400;
    angles[7]  = 17'h00200;// i=4~7
    angles[8]  = 17'h00100;
    angles[9]  = 17'h00080;
    angles[10] = 17'h00040;
    angles[11] = 17'h00020;// i=8~11
    angles[12] = 17'h00010;
    angles[13] = 17'h00008;
    angles[14] = 17'h00004;
    angles[15] = 17'h00002;// i=12~15
    angles[16] = 17'h00001;
end

reg signed [32:0]x,y; 
reg signed [32:0]x_next,y_next;
reg signed [17:0] angle;
integer i;

always@(*)begin
 
    x={K,16'b0};
    y=33'h0;
    angle={1'b0,theta};
   
    for(i=0;i<16;i=i+1)begin
        if(!angle[17])begin  
        
            x_next=x-(y>>>i); 
            y_next=y+(x>>>i);
            angle=angle-{1'b0,angles[i]};
        end else begin
          
            x_next=x+(y>>>i);
            y_next=y-(x>>>i);
            angle=angle+{1'b0,angles[i]};
        end
        x=x_next;
        y=y_next;
    end
end

assign sin_out = y[32:16];
assign cos_out = x[32:16];

endmodule
