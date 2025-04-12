* RC Bandpass Filter SPICE Netlist
* Center Frequency: 100Hz, Bandwidth: 40Hz

Vin in 0 AC 1.0
C1 in mid 1.9408e-07
R1 mid 0 10000
R2 mid out 10000
C2 out 0 1.3046e-07
Rload out 0 100k

.ac dec 100 10.0 1000.0
.print ac v(out)
.measure AC max_out max v(out)
.measure AC f_lower when v(out)=max_out/sqrt(2) rise=1
.measure AC f_upper when v(out)=max_out/sqrt(2) fall=1

.end