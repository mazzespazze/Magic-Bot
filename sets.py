import random
sets = {"No Name":              "e:arn or e:atq or e:leq or e:drk or e:fem or e:hml",
        "Ice Age":              "e:ice or e:all",
        "Mirage":               "e:mis or e:vis or e:wth",
        "Tempest":              "e:tmp or e:sth or e:exo",
        "Urza":                 "e:usg or e:ulg or e:uds",
        "Masques":              "e:mmq or e:nem or e:pcy",
        "Invasion":             "e:inv or e:pls or e:apc",
        "Odyssey":              "e:ody or e:tor or e:jud",
        "Onslaught":            "e:ons or e:lgn or e:scg",
        "Mirrodin":             "e:mrd or e:dst or e:5dn",
        "Kamigawa":             "e:chk or e:bok or e:sok",
        "Ravnica":              "e:rav or e:gpt or e:dis",
        "Coldsnap":             "e:csp",
        "Time Spiral":          "e:tsp or e:plc or e:fut",
        "Lorwyn":               "e:lrw or e:mor",
        "Shadowmoor":           "e:shm or e:eve",
        "Alara":                "e:ala or e:con or e:arb",
        "Zendikar":             "e:zen or e:wwk or e:roe",
        "Scars of Mirrodin":    "e:som or e:mbs or e:nph",
        "Innistrad":            "e:isd or e:dka or e:avr",
        "Return to Ravnica":    "e:rtr or e:gtc or e:dgm",
        "Theros":               "e:ths or e:bng or e:jou",
        "Khans of Tarkir":      "e:ktk or e:frf or e:dtk",
        "Battle for Zendikar":  "e:bfz or e:ogw",
        "Shadows over Innistrad":"e:soi or e:emn",
        "Kaladesh":             "e:kld or e:aer",
        "Amonkhet":             "e:akh or e:hou",
        "Ixalan":               "e:xln or e:rix",
        "Post":                 "e:dom or e:grn"}

def get_sets(number_sets=2):
    if number_sets <= 0: return "You're funny..."
    exps,values = '',[]
    ks,vs,ret = list(sets.keys()),list(sets.values()),[]
    for x in range(number_sets):#first it selects the expansion title
        new_val = random.randint(0,len(ks)-1)
        if new_val in values: continue
        values.append(new_val),ret.append(ks[values[x]]),ret.append(vs[values[x]])
    exps = " - ".join(map(str,ret[0::2])) + "\n(" + " or ".join(map(str,ret[1::2])) + ")"
    return exps

if __name__ == '__main__':
    print(get_sets(2))
