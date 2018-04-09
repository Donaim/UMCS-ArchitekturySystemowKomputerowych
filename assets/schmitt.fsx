// rezystory
let R0 = [ 55.0; 5.039; 2.940; 0.560; 55.0; 55.0 ] // kilo-omy

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

printfn "U0 = %0.2f; U1 = %0.2f" UQ1B_MIN UQ2B_MIN

// find R2, R3
let U1 = 1.40
let U0  = 1.10
let R3 = ((((U1 - UBE) / R(4)) / UZ) ** -1.0) - R(4) |> (fun x -> (int)x)
let R2 = ((((U0  - UBE) / R(4)) / UZ) ** -1.0) - R(4) |> (fun x -> (int)x)

printfn "R2 = %d; R3 = %d" R2 R3