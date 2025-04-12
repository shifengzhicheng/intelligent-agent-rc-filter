# SPICE Netlist Generator
# Converts RC filter component values into a SPICE netlist for simulation

class NetlistGenerator:
    def __init__(self):
        """
        Initialize the SPICE netlist generator
        """
        pass
        
    def generate_bandpass_netlist(self, component_values, vin=1.0, freq_start=1, freq_stop=1000, points_per_decade=100):
        """
        Generate a SPICE netlist for a passive RC bandpass filter
        
        Args:
            component_values (dict): Dict containing component values (R1, R2, C1, C2, etc.)
            vin (float): Input voltage amplitude
            freq_start (float): Start frequency for AC analysis in Hz
            freq_stop (float): Stop frequency for AC analysis in Hz
            points_per_decade (int): Number of points per decade for AC analysis
            
        Returns:
            str: Complete SPICE netlist
        """
        # Extract component values, with error handling for missing components
        r1 = component_values.get('R1', 1000)
        r2 = component_values.get('R2', 1000)
        c1 = component_values.get('C1', 1e-6)
        c2 = component_values.get('C2', 1e-6)
        
        # Create the netlist
        netlist = []
        netlist.append("* RC Bandpass Filter SPICE Netlist")
        netlist.append("* Center Frequency: 100Hz, Bandwidth: 40Hz")
        netlist.append("")
        
        # Input voltage source
        netlist.append(f"Vin in 0 AC {vin}")
        
        # High-pass section (C1, R1)
        netlist.append(f"C1 in mid {c1}")
        netlist.append(f"R1 mid 0 {r1}")
        
        # Low-pass section (R2, C2)
        netlist.append(f"R2 mid out {r2}")
        netlist.append(f"C2 out 0 {c2}")
        
        # Load resistor (optional)
        netlist.append("Rload out 0 100k")
        
        # Analysis commands
        netlist.append("")
        netlist.append(f".ac dec {points_per_decade} {freq_start} {freq_stop}")
        netlist.append(".print ac v(out)")
        
        # 修复测量命令 - 使用正确的ngspice语法
        netlist.append(".measure AC max_out max v(out)")
        netlist.append(".measure AC f_lower when v(out)=max_out/sqrt(2) rise=1")
        netlist.append(".measure AC f_upper when v(out)=max_out/sqrt(2) fall=1")
        
        # End the netlist
        netlist.append("")
        netlist.append(".end")
        
        return "\n".join(netlist)

    def save_netlist(self, netlist, filename="rc_bandpass.sp"):
        """
        Save the SPICE netlist to a file
        
        Args:
            netlist (str): The SPICE netlist
            filename (str): Path to save the netlist
            
        Returns:
            str: Path to the saved file
        """
        with open(filename, 'w') as f:
            f.write(netlist)
        return filename