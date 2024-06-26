from converter.animation.Stage import ActorStage
import re

## NOTE: this still relying on older script. we only need the gender info for instances when the json has "type" as gender for an actor
## in those instances only is the source file of any use anymore; see original.py ("SOURCE TXT PARSER" section)
## for the rest of the data, we instead rely on SLAL jsons now which is always present (see "SLAL JSON PARSER" section)
## this applies to all the stuff in animation folder i think, sowwy :)

##t hat's fine - I'll keep this parser anyway just in case it becomes more useful again.

class Actor:
    def __init__(self, number, scene_name):
        self.scene_name = scene_name
        self.number = number
        self.stages: dict[str, ActorStage] = {}
        self.gender: str = None
        self.args = {}

        self.current_stage: ActorStage = None
        self.in_actor = False


    def get_name(self):
        return f"a{self.number}"
        
    def parse_line(self, line):
        if actor_match:= re.search(r'actor\s*(\d+)\s*=\s*([^()]+)\(([^)]*)\)', line):

            if(actor_match.group(1) == self.number):
                self.in_actor = True
                self.gender = actor_match.group(2)
                actor_args = actor_match.group(3)

                args = re.findall(r'(\w+)=(?:"([^"]*)"|([^,)]+))', actor_args)

                for arg, value1, value2 in args:
                    value = value1 if value1 else value2
                    self.args[arg] = value
            else:
                self.in_actor = False


        elif stage_match := re.search(r'Stage\((\d+),\s*([^)]*)\)', line):
            if(self.in_actor):
                stage_info = stage_match.groups()
                stage_number = int(stage_info[0])
                stage = ActorStage(stage_number)

                attributes = re.findall(r'(\w+)\s*=\s*("[^"]+"|[^,)]+)', stage_info[1])
                stage.process_attributes(attributes)

                animvars_match = re.search(r'animvars="([^"]*)"', stage_info[1])
                if animvars_match:
                    stage.animvars = animvars_match.group(1)
            
                self.stages[stage.name] = stage

        elif re.search(r'\bstage_params\s*=', line):
            self.in_actor = False

        