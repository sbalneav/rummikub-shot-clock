"""Build the Rummikub Shot Clock PCB (unrouted) with the KiCad 9 pcbnew API."""
import os, sys
import pcbnew
from pcbnew import FromMM as mm, VECTOR2I

FP = os.environ["FPDIR"]
OUT = sys.argv[1]
OX, OY = 100.0, 100.0          # board origin offset in mm
W, H = 72.0, 58.0              # board size in mm

b = pcbnew.BOARD()
ds = b.GetDesignSettings()
nc = ds.m_NetSettings.GetDefaultNetclass()
nc.SetTrackWidth(mm(0.4)); nc.SetClearance(mm(0.25))
nc.SetViaDiameter(mm(0.9)); nc.SetViaDrill(mm(0.45))

nets = {}
def net(name):
    if name not in nets:
        n = pcbnew.NETINFO_ITEM(b, name); b.Add(n); nets[name] = n
    return nets[name]

LIB = {
 "DIP8":  ("Package_DIP", "DIP-8_W7.62mm_Socket"),
 "R":     ("Resistor_THT", "R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal"),
 "TRIM":  ("Potentiometer_THT", "Potentiometer_Bourns_3296W_Vertical"),
 "CP":    ("Capacitor_THT", "CP_Radial_D6.3mm_P2.50mm"),
 "C":     ("Capacitor_THT", "C_Disc_D5.0mm_W2.5mm_P5.00mm"),
 "CF":    ("Capacitor_THT", "C_Rect_L7.2mm_W3.5mm_P5.00mm_FKS2_FKP2_MKS2_MKP2"),
 "TO92":  ("Package_TO_SOT_THT", "TO-92_Inline_Wide"),
 "D":     ("Diode_THT", "D_DO-35_SOD27_P7.62mm_Horizontal"),
 "H2":    ("Connector_PinHeader_2.54mm", "PinHeader_1x02_P2.54mm_Vertical"),
 "H3":    ("Connector_PinHeader_2.54mm", "PinHeader_1x03_P2.54mm_Vertical"),
 "MH":    ("MountingHole", "MountingHole_3.2mm_M3"),
}

def place(ref, kind, value, x, y, rot, pads):
    lib, name = LIB[kind]
    f = pcbnew.FootprintLoad(os.path.join(FP, lib + ".pretty"), name)
    f.SetReference(ref); f.SetValue(value)
    f.SetPosition(VECTOR2I(mm(OX + x), mm(OY + y)))
    f.SetOrientationDegrees(rot)
    f.Value().SetVisible(False)
    for p in f.Pads():
        n = pads.get(p.GetNumber())
        if n: p.SetNet(net(n))
    b.Add(f)
    return f

V, G = "+3V", "GND"
# Rotation: 0 = pin 1 left, pin 2 to the right (+x). 90 = pin 2 above pin 1. 270 = pin 2 below.
# DIP origin is pin 1; pins 1-4 run down (+y), pins 8-5 are 7.62 mm to the right.

# ---- power / off-board connectors along the top edge
place("J1", "H2", "BATTERY", 4, 4, 270, {"1": "VBAT", "2": G})        # pin1 top
place("J2", "H2", "POWER_SW", 12, 4, 270, {"1": "VBAT", "2": V})
place("J3", "H2", "EASY_BTN", 20, 4, 270, {"1": "BTN", "2": G})
place("J4", "H2", "SPEAKER", 66, 4, 270, {"1": V, "2": "SPK_N"})
place("C6", "CP", "220uF", 28, 6, 0, {"1": V, "2": G})

# ---- timer U1
place("U1", "DIP8", "TLC555", 10, 24, 0,
      {"1": G, "2": "TIMING", "3": "OUT1", "4": V, "5": "CV1", "6": "TIMING", "7": "", "8": V})
place("R1", "R", "150k", 2, 41, 90, {"1": "RT1", "2": V})
place("VR1", "TRIM", "250k", 9.5, 45, 0, {"1": "RT1", "2": "TIMING", "3": "TIMING"})
place("C1", "CP", "220uF", 13, 39.5, 0, {"1": "TIMING", "2": G})
place("R3", "R", "22R", 2, 14, 0, {"1": "BTN", "2": "TIMING"})
place("C2", "C", "10nF", 20.5, 34.5, 0, {"1": "CV1", "2": G})
place("C8", "C", "100nF", 10, 18.5, 0, {"1": V, "2": G})

# ---- inverter
place("R4", "R", "10k", 21, 18.5, 0, {"1": "OUT1", "2": "B1"})
place("Q1", "TO92", "2N3904", 25, 26, 0, {"1": G, "2": "B1", "3": "ALARM"})
place("R5", "R", "100k", 24, 14, 0, {"1": V, "2": "ALARM"})

# ---- jumper: 1-2 steady tone, 2-3 pulsed
place("JP1", "H3", "STEADY/PULSE", 28.5, 35.5, 90, {"1": "ALARM", "2": "RST2", "3": "PULSE"})

# ---- tone U2
place("U2", "DIP8", "TLC555", 39, 24, 0,
      {"1": G, "2": "TH2", "3": "OUT2", "4": "RST2", "5": "CV2", "6": "TH2", "7": "DIS2", "8": V})
place("R6", "R", "1k", 36, 14, 0, {"1": V, "2": "DIS2"})
place("R7", "R", "10k", 37, 38, 0, {"1": "DIS2", "2": "TH2"})
place("C3", "C", "47nF", 36.5, 43.5, 0, {"1": "TH2", "2": G})
place("C4", "C", "10nF", 49.5, 41, 90, {"1": "CV2", "2": G})
place("C9", "C", "100nF", 39, 18.5, 0, {"1": V, "2": G})

# ---- pulser U3
place("U3", "DIP8", "TLC555", 58, 24, 0,
      {"1": G, "2": "TH3", "3": "PULSE", "4": "ALARM", "5": "CV3", "6": "TH3", "7": "DIS3", "8": V})
place("R10", "R", "10k", 57.5, 14, 0, {"1": V, "2": "DIS3"})
place("R11", "R", "330k", 56, 38, 0, {"1": "DIS3", "2": "TH3"})
place("C5", "CF", "1uF film", 55, 43.5, 0, {"1": "TH3", "2": G})
place("C7", "C", "10nF", 69.5, 41, 90, {"1": "CV3", "2": G})
place("C10", "C", "100nF", 58, 18.5, 0, {"1": V, "2": G})

# ---- speaker driver
place("R8", "R", "680R", 48, 9, 0, {"1": "OUT2", "2": "B2"})
place("Q2", "TO92", "2N2222A", 48.5, 14, 0, {"1": G, "2": "B2", "3": "SPK_C"})
place("R9", "R", "10R", 60, 9, 0, {"1": "SPK_N", "2": "SPK_C"})
place("D1", "D", "1N4148", 46, 4, 0, {"1": V, "2": "SPK_N"})    # pad 1 = cathode

place("H1", "MH", "M3", 3.5, 3.5 + 25, 0, {})
place("H2", "MH", "M3", 67.5, 46, 0, {})

# ---- reference text tweaks (silkscreen clean-up)
def ref_at(ref, x, y, rot=0, hide=False):
    f = b.FindFootprintByReference(ref)
    t = f.Reference()
    if hide: t.SetVisible(False); return
    t.SetPosition(VECTOR2I(mm(OX + x), mm(OY + y))); t.SetTextAngleDegrees(rot)
for r in ("J1", "J2", "J3", "J4"): ref_at(r, 0, 0, hide=True)
ref_at("R1", 4.6, 37.2, 90)
ref_at("C8", 7.4, 18.5); ref_at("C9", 36.4, 18.5); ref_at("C10", 55.0, 18.5)
ref_at("Q2", 46.0, 14.0)
ref_at("JP1", 31.0, 33.5)

# ---- board outline
def seg(x1, y1, x2, y2):
    s = pcbnew.PCB_SHAPE(b); s.SetShape(pcbnew.SHAPE_T_SEGMENT)
    s.SetStart(VECTOR2I(mm(OX + x1), mm(OY + y1))); s.SetEnd(VECTOR2I(mm(OX + x2), mm(OY + y2)))
    s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(mm(0.1)); b.Add(s)
for a in [(0, 0, W, 0), (W, 0, W, H), (W, H, 0, H), (0, H, 0, 0)]: seg(*a)

pcbnew.SaveBoard(OUT, b)
print("saved", OUT, "nets:", len(nets))
