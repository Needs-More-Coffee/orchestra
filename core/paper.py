import os

class Paper:
    def __init__(self):
        self.entries = []

    def write_system(self, content):
        self.entries.append({
            "source": "{SYSTEM}",
            "content": content,
            "flag": "",
            "compliance": "",
            "tags": []
        })

    def write_voice(self, voice_name, content, flag="", compliance=""):
        self.entries.append({
            "source": voice_name,
            "content": content,
            "flag": flag,
            "compliance": compliance,
            "tags": []
        })

    def classify(self, target_source, tagger, tag, reason):
        tag_string = f"{tagger} | {tag} - {reason}"
        for entry in reversed(self.entries):
            if entry["source"] == target_source:
                if tag_string not in entry["tags"]:
                    entry["tags"].append(tag_string)
                return True
        return False

    def replace_tag(self, target_source, old_tag, new_tag):
        for entry in reversed(self.entries):
            if entry["source"] == target_source:
                for i, tag_string in enumerate(entry["tags"]):
                    if old_tag in tag_string:
                        if new_tag is None:
                            entry["tags"].pop(i)
                        else:
                            entry["tags"][i] = tag_string.replace(old_tag, new_tag)
                        return True
        return False

    def resolve_halt(self, target_source):
        for entry in reversed(self.entries):
            if entry["source"] == target_source:
                for i, tag_string in enumerate(entry["tags"]):
                    if "{Halt}" in tag_string and "(Resolved)" not in tag_string:
                        entry["tags"][i] = tag_string + " (Resolved)"
                        return True
        return False

    def has_unreviewed_vio2(self):
        for entry in self.entries:
            for tag_string in entry["tags"]:
                if "{Vio2}" in tag_string:
                    return entry["source"]
        return None

    def has_unreviewed_halt(self):
        for entry in self.entries:
            for tag_string in entry["tags"]:
                if "{Halt}" in tag_string and "(Resolved)" not in tag_string:
                    return entry["source"]
        return None

    def save_violation(self, voice_name, content, session_id):
        os.makedirs("violations", exist_ok=True)
        filepath = f"violations/violation_{voice_name}_{session_id}.md"
        with open(filepath, 'a') as f:
            f.write(content)
            f.write("\n\n---\n\n")

    def as_string(self):
        result = ""
        for entry in self.entries:
            result += f"-{entry['source']}-\n"
            if entry.get("compliance"):
                result += f"**Compliance:** {entry['compliance']}\n"
            result += f"**Source:** {entry['source']}\n"
            result += f"**Flag:** {entry.get('flag', '')}\n"
            tag_field = " | ".join(entry["tags"]) if entry.get("tags") else ""
            result += f"**Tag:** {tag_field}\n"
            result += f"**Content:** {entry['content']}\n"
            result += "---\n"
        return result

    def save(self, filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(self.as_string())
