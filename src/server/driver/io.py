class Io:
    ManualDrive = "manualdrive"

    class Cutter:
        EndstopUpper = "cenuppr"
        EndstopLower = "cenlower"
        Upper = "ftSwarm55.Stepper1"
        Lower = "ftSwarm55.Stepper2"
        VChain = "ftSwarm200.Stepper4"
        VChainEndstop = "ftSwarm102.A2"
        Rotation = "ftSwarm55.Stepper3"
        RotationEndstop = "ftSwarm102.A1"
        Relais = "relay"

    class Centerer:
        Compressor = "xcompr"
        MagnetValve = "xmvalve"

    class Scanner:
        ScannerStepper = "ftSwarm200.Stepper1"
