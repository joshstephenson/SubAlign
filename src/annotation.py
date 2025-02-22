from difflib import SequenceMatcher


class Annotation:
    class Language:
        def __init__(self, subtitles, utterance, is_source=True):
            self.is_source = is_source
            self.subtitles = subtitles
            self.utterance = utterance

        def lines(self) -> str:
            return "\n\n".join(s.lines for s in self.subtitles)

        def get_offsets_and_length(self, line):
            """
            returns y,x and length for curses highlighting
            """
            match = SequenceMatcher(None, self.utterance, line).find_longest_match()
            y_offset = 0
            length = match.size
            x_offset = match.b
            y_offset += 1

            return y_offset, x_offset, length

        def has_subtitles(self) -> bool:
            return len(self.subtitles) > 0

        def has_utterance(self) -> bool:
            return self.utterance is not None

    def __init__(self, source_subs, target_subs, source_utterance, target_utterance):
        self.source = Annotation.Language(source_subs, source_utterance, is_source=True)
        self.target = Annotation.Language(target_subs, target_utterance, is_source=False)

    def has_empty_source(self) -> bool:
        return self.source.utterance is None

    def has_empty_target(self) -> bool:
        return self.target.utterance is None

    def content_length(self) -> int:
        if self.has_empty_source() and self.has_empty_target():
            return 0
        elif self.has_empty_target():
            return len(self.source.utterance)
        elif self.has_empty_source():
            return len(self.target.utterance)
        else:
            return max(len(self.source.utterance), len(self.target.utterance))

    def order(self) -> int:
        return min([sub.index for sub in self.source.subtitles])

    def is_stranded(self) -> bool:
        return self.source.utterance is None and self.target.utterance is None
