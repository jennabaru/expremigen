from midiutil import MIDIFile

from expremigen.io.constants import PhraseProperty as PP
from expremigen.io.phrase import Phrase
from expremigen.patterns.pchord import Pchord


class Pat2Midi:
    def __init__(self, numTracks=1, removeDuplicates=True, deinterleave=True, file_format=1):
        self.midiFile = MIDIFile(numTracks=numTracks, removeDuplicates=removeDuplicates, deinterleave=deinterleave,
                                 adjust_origin=False, file_format=file_format)

    def setTempo(self, tempo=100, time=0):
        self.midiFile.addTempo(track=0, time=time, tempo=tempo)

    def addPhrase(self, phrase: Phrase, track=0, channel=0, start_time=0):
        for event in phrase:
            if isinstance(event[PP.NOTE], Pchord):
                for n in event[PP.NOTE].notes:
                    self.midiFile.addNote(
                        track=track,
                        channel=channel,
                        pitch=n,
                        time=start_time + phrase.generated_duration() + event[PP.LAG],
                        duration=event[PP.DUR] * event[PP.PLAYEDDUR],
                        volume=event[PP.VOL],
                        annotation=None)
            else:
                self.midiFile.addNote(
                    track=track,
                    channel=channel,
                    pitch=event[PP.NOTE],
                    time=start_time + phrase.generated_duration() + event[PP.LAG],
                    duration=event[PP.DUR] * event[PP.PLAYEDDUR],
                    volume=event[PP.VOL],
                    annotation=None)
        return phrase.generated_duration()

    def addPhrases(self, list_of_phrase, track=0, channel=0, start_time=0):
        time_delta = 0
        for phrase in list_of_phrase:
            duration = self.addPhrase(phrase, track, channel, start_time + time_delta)
            time_delta += duration
        return start_time + time_delta

    def write(self, filename):
        try:
            with open(filename, "wb") as f:
                self.midiFile.writeFile(fileHandle=f)
        except Exception as e:
            print("we hit a SNAFU while writing to {0}: {1}".format(filename, e))
