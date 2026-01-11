# worldcodex_art
A CLI interface to generate artwork from a world description

#test

#Load your bible:
worldcodex-art world load-json /home/ubuntu/projects/worldcodex/worlds/titan-osa/views/world_bible.json

#Confirm stored:
worldcodex-art world show

#See styles:
worldcodex-art art styles

# Set a style:
worldcodex-art art set --style industrial_amber --size 1024x1024 --intent concept
worldcodex-art art show

# Preview prompt:
worldcodex-art world list places

worldcodex-art world show place lantern_walk_corridor

worldcodex-art prompt preview --place lantern_walk_corridor "Procession at peak crowd"

worldcodex-art prompt preview --place lantern_walk_corridor --motif frost_and_condensation "Procession at peak crowd"

#gen images with opemai  (default style, size)
worldcodex-art provider set openai
worldcodex-art image gen --place lantern_walk_corridor --motif frost_and_condensation --n 2 --out outputs/openai  "Procession at peak crowd"

# gen with character - characyter must exist in world json
worldcodex-art image gen --place aegis_life_support_bay --character example_engineer "Shift change inspection"

# test openai image link

python - <<'PY'
from openai import OpenAI
client = OpenAI()
print("client ok:", bool(client))
PY

# testing

# run pytest scripts

# python -m pytest -rs

