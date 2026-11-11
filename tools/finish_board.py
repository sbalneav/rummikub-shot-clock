"""Import the routed session, add silkscreen labels and a ground pour, fill zones, save."""
import sys
import pcbnew
from pcbnew import FromMM as mm, VECTOR2I

src, ses, out = sys.argv[1:4]
OX, OY, W, H = 100.0, 100.0, 72.0, 58.0
b = pcbnew.LoadBoard(src)
assert pcbnew.ImportSpecctraSES(b, ses), "SES import failed"

def text(s, x, y, size=1.0, layer=pcbnew.F_SilkS, rot=0, bold=False):
    t = pcbnew.PCB_TEXT(b)
    t.SetText(s); t.SetLayer(layer)
    t.SetPosition(VECTOR2I(mm(OX + x), mm(OY + y)))
    t.SetTextSize(VECTOR2I(mm(size), mm(size)))
    t.SetTextThickness(mm(size * (0.2 if bold else 0.15)))
    t.SetTextAngleDegrees(rot)
    if layer == pcbnew.B_SilkS: t.SetMirrored(True)
    b.Add(t)

# connector labels (pads sit at y=4; labels just below)
for lbl, x in (("BAT+ -", 5.3), ("ON/OFF", 13.3), ("BUTTON", 21.3), ("SPKR", 67.3)):
    text(lbl, x, 1.7, 0.9)
text("1-2 STEADY", 31.0, 37.5, 0.8)
text("2-3 PULSE", 31.0, 38.9, 0.8)
text("E B C", 27.5, 29.2, 0.8)
text("E B C", 51.0, 17.2, 0.8)
# credits in the bottom strip, both sides
text("RUMMIKUB SHOT CLOCK  rev A", W / 2, 51.2, 1.4, bold=True)
text("3 V: TLC555 x3   or   4.5-9 V: NE555 x3", W / 2, 53.6, 0.9)
text("Designed with Claude (Anthropic)   CERN-OHL-P v2", W / 2, 55.6, 0.9)
text("RUMMIKUB SHOT CLOCK  rev A", W / 2, 52.0, 1.4, pcbnew.B_SilkS, bold=True)
text("Designed with Claude (Anthropic)", W / 2, 54.6, 1.0, pcbnew.B_SilkS)

# ground pour on the back copper
gnd = b.FindNet("GND")
z = pcbnew.ZONE(b)
z.SetLayer(pcbnew.B_Cu); z.SetNet(gnd)
z.SetLocalClearance(mm(0.4)); z.SetMinThickness(mm(0.3))
z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
z.SetThermalReliefGap(mm(0.3)); z.SetThermalReliefSpokeWidth(mm(0.6))
ol = z.Outline(); ol.NewOutline()
m = 0.5
for x, y in [(m, m), (W - m, m), (W - m, H - m), (m, H - m)]:
    ol.Append(mm(OX + x), mm(OY + y))
b.Add(z)
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
pcbnew.SaveBoard(out, b)
print("saved", out, "tracks:", len(b.GetTracks()))
