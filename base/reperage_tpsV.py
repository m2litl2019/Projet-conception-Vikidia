from texteval import load

def reperage_tps(target):
    data = load(target)
    tps = {}
    pos = {}
    for sentence in data:
        for word in sentence:

            if word.pos.startswith("V"):
                if word.pos == "VINF":
                    tps["TENSE_COUNT_VINF"] = tps.get("TENSE_COUNT_VINF",0) + 1
                elif word.pos == "VPP":
                    tps["TENSE_COUNT_VPP"] = tps.get("TENSE_COUNT_VPP",0) + 1
                else:
                    if word.tense is not None:
                        tps["TENSE_COUNT_V"+word.tense] = tps.get("TENSE_COUNT_V"+word.tense,0) + 1
            else:
                pos["POS_COUNT_"+word.pos] = pos.get("POS_COUNT_"+word.pos,0) + 1

    tps.update(pos)
    return(tps)

if __name__== "__main__" :
    reperage_tps("ema.tal")

