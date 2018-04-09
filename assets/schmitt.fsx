// simul: http://tinyurl.com/y72el3aa  

// rezystory
let R0 = [ 100.0; 4.7; 2.2; 0.5; 100.0; 100.0 ] // kilo-omy

// const
let UZ = 5.0
let UBE = 0.6
let R1 = R0 |> List.map ((fun x -> x * 1000.0) >> (fun x -> (int)x))
let R index = (float)R1.[index - 1]

// Q2
let UQ2B = R(6) / (R(2) + R(5) + R(6)) * UZ
let UQ2E_MAX = UQ2B - UBE
let UQ2E = R(4) / (R(3) + R(4)) * UZ
let UQ2B_MIN = UQ2E + UBE

// Q1
let UQ1E = R(4) / (R(2) + R(4)) * UZ
let UQ1B_MIN = UQ1E + UBE

// find R2, R3
let U1 = UQ2B_MIN
let U0  = UQ1B_MIN
let R3 = ((((U1 - UBE) / R(4)) / UZ) ** -1.0) - R(4) |> (fun x -> (int)x)
let R2 = ((((U0  - UBE) / R(4)) / UZ) ** -1.0) - R(4) |> (fun x -> (int)x)

