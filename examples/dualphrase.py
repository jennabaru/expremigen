from expremigen.io.constants import PhraseProperty as PP
from expremigen.io.pat2mid import Pat2Mid
from expremigen.io.phrase import Phrase
from expremigen.musicalmappings.durations import Durations as Dur
from expremigen.musicalmappings.dynamics import Dynamics as Dyn
from expremigen.musicalmappings.note2midi import Note2Midi
from expremigen.patterns.pconst import Pconst
from expremigen.patterns.pseq import Pseq
from expremigen.patterns.ptween import Ptween

outputfile = "output/dualphrase.mid"


def create_phrase():
    n = Note2Midi()
    notes = ["c4", "e4", "g4", "c5", "b4", "g4", "f4", "d4", "c4"]
    from vectortween.NumberAnimation import NumberAnimation
    from vectortween.SequentialAnimation import SequentialAnimation
    increase = NumberAnimation(frm=Dyn.mp, to=Dyn.f)
    decrease = NumberAnimation(frm=Dyn.f, to=Dyn.ppp)
    swell_dim = SequentialAnimation([increase, decrease])
    increasing_staccato = NumberAnimation(frm=1, to=0.5)
    properties1 = {
        # convert from note names to midi numbers
        PP.NOTE: Pseq(n.convert2(notes)),
        # last note is longer than the rest
        PP.DUR: Pseq([Pconst(Dur.quarter, len(notes) - 1), Pconst(Dur.whole, 1)]),
        # animate staccato
        PP.PLAYEDDUR: Ptween(increasing_staccato, 0, 0, len(notes), len(notes)),
        # volume should linearly go up from mp to f, then go down from f to ppp as the phrase progresses
        PP.VOL: Ptween(swell_dim, 0, 0, len(notes), len(notes), None),
    }
    properties2 = {
        # convert from (reversed) note names to midi numbers
        PP.NOTE: Pseq(n.convert2(notes[::-1])),
        # last note is longer than the rest
        PP.DUR: Pseq([Pconst(Dur.quarter, len(notes) - 1), Pconst(Dur.whole, 1)]),
        # animate staccato
        PP.PLAYEDDUR: Ptween(increasing_staccato, 0, 0, len(notes), len(notes)),
        # volume should linearly go up from mp to f, then go down from f to ppp as the phrase progresses
        PP.VOL: Ptween(swell_dim, 0, 0, len(notes), len(notes), None),
    }

    p1 = Phrase(properties1)
    p2 = Phrase(properties2)
    p2m = Pat2Mid()
    p2m.setTempo(120)
    total_dur = p2m.addPhrases([p1,p2])
    print(total_dur)
    p2m.write(outputfile)


if __name__ == "__main__":
    create_phrase()