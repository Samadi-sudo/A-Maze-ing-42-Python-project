import parsing
import ascii
import prim
import kruskal
config = parsing.parsing()

# main(HEIGHT, WIDTH, ENTRY, EXIT, OUTPUT_FILE, PERFECT,SEED)
print(config)
if config["algorithm"] == "prims":
    algo = prim.generator
else:
    algo = kruskal.generator
ascii.main(config["HEIGHT"],config["WIDTH"], config["ENTRY"], config["EXIT"], config["OUTPUT_FILE"], config["PERFECT"], config.get('seed', None),algo)