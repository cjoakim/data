# Instances of this class are used to reduce a given dictionary
# object, such as a Cosmos DB or MongoDB document, to only the
# pertinent attributes per the specified inclusions and exclusions.
# Chris Joakim, 2025


class DocFilter:
    def __init__(self, include_attrs: list, exclude_attrs: list):
        if include_attrs is None:
            self.include_attrs = set()
        else:
            self.include_attrs = set(include_attrs)

        if exclude_attrs is None:
            self.exclude_attrs = set()
        else:
            self.exclude_attrs = set(exclude_attrs)

    def filter(self, doc: dict):
        filtered = dict()
        if len(self.include_attrs) == 0:
            for attr in doc.keys():
                if attr not in self.exclude_attrs:
                    filtered[attr] = doc[attr]
        else:
            for attr in self.include_attrs:
                if attr in doc.keys():
                    if attr not in self.exclude_attrs:
                        filtered[attr] = doc[attr]

        return filtered
