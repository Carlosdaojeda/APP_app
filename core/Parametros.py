phi = 0.234 
mu = 0.5      
ct = 15e-6    
k = 10        
L = 2500      
b = 300       
h = 12        
B = 1.2       
pi = 3000     
pwf = 600     

# --- Parámetros derivados ---
eta = 0.00633 * k / (phi * mu * ct)   
delta_p = pi - pwf
A = b * h  
conversion_factor = 0.001127 * k * A / (mu * B * L)  
