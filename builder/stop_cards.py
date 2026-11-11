# Text for each stop card. The voice agent repeats this text as fact,
#source URL: https://www.nasa.gov/missions/mars-science-laboratory/curiosity-rover/NASAs-curiosity-rover-sees-martian-spiderwebs-up-close/ 
#source URL: https://science.nasa.gov/blog/curiosity-blog-sols-4804-4811-kicking-off-the-final-phase-of-boxwork-exploration
# so EVERY sentence must be backed by a source in "sources".
# NOTE_to_the_team: Abdelhamid must check it against the sources before we publish, i already chekced it but it needs a double check as required in my task.

NASA_BOXWORK = "NASA, Curiosity Rover Sees Martian Spiderwebs Up Close, 2026-02-23"
RAD_SOURCE = "Curiosity RAD, average surface dose rate (SwRI, Hassler et al. 2013)"

CARDS = {
    0: {
        "task": "Check your suit and oxygen, then look ahead at the first ridges.",
        "hazard": "Slope here is 6.5 degrees, under the 12 degree safety limit: walk normally.",
        "science": (
            "Boxwork is a network of low ridges about 1 to 2 meters tall with "
            "sandy hollows between them; scientists think groundwater flowed "
            "through cracks in the rock and left minerals behind."
        ),
        "sources": [
            "MSL waypoints",
            "Navcam sol 4596",
            "Curiosity REMS, daily mean air temperature, sol 4596",
            RAD_SOURCE,
            NASA_BOXWORK,
        ],
    },
    1: {
        "task": "Look closely at the ridge rock for small round bumps called nodules.",
        "hazard": (
            "Slope here is 9.9 degrees, under the 12 degree safety limit, "
            "but steeper than at base: walk carefully."
        ),
        "science": (
            "Pea-sized bumps called nodules in the boxwork are minerals "
            "left behind by groundwater."
        ),
        "sources": [
            "MSL waypoints",
            "Navcam sol 4618",
            "Curiosity REMS, daily mean air temperature, sol 4618",
            RAD_SOURCE,
            NASA_BOXWORK,
        ],
    },
    2: {
        "task": "Photograph the ridge from a safe spot; do not climb it.",
        "hazard": (
            "Steep slope: 15 degrees, above the 12 degree safety limit. "
            "Walk slowly and watch your footing."
        ),
        "science": "Samples NASA drilled from a boxwork ridge contained clay minerals.",
        "sources": [
            "MSL waypoints",
            "Navcam sol 4639",
            "Curiosity REMS, daily mean air temperature, sol 4639",
            RAD_SOURCE,
            NASA_BOXWORK,
        ],
    },
        3: {
        "task": "Check the ground for loose sand before you step; do not rush.",
        "hazard": (
            "Slope here is 4.7 degrees, nearly flat. The hollows between "
            "ridges are sandy: test the ground before you step."
        ),
        "science": (
            "A sample NASA drilled from bedrock in a boxwork hollow "
            "contained carbonate minerals."
        ),
        "sources": [
            "MSL waypoints",
            "Navcam sol 4655",
            "Curiosity REMS, daily mean air temperature, sol 4655",
            RAD_SOURCE,
            NASA_BOXWORK,
        ],
    },
        4: {
        "task": "Photograph the ridges and hollows around you and note anything unusual.",
        "hazard": (
            "Slope here is 11 degrees, just under the 12 degree safety limit, "
            "and nearby points reach 12 to 14 degrees: watch your footing."
        ),
        "science": (
            "Curiosity's main exploration of the boxwork ran from about sol 4600 "
            "to sol 4805, and this stop is inside that period."
        ),
        "sources": [
            "MSL waypoints",
            "Navcam sol 4711",
            "Curiosity REMS, daily mean air temperature, sol 4711",
            RAD_SOURCE,
            "NASA, Curiosity Blog Sols 4804-4811, A. Fraeman, 2026-02-13",
        ],
    },
        5: {
        "task": "Take a last photo of the boxwork, then check your oxygen and start the walk back to base.",
        "hazard": (
            "Slope here is 3.7 degrees, nearly flat. "
            "Check your oxygen before the walk back to base."
        ),
        "science": (
            "Around sol 4805, Curiosity began its final phase in the boxwork: "
            "last measurements of ridges and hollows, and a look at where the "
            "boxwork meets the neighboring rock layers."
        ),
        "sources": [
            "MSL waypoints",
            "Navcam sol 4820",
            "Curiosity REMS, daily mean air temperature, sol 4820",
            RAD_SOURCE,
            "NASA, Curiosity Blog Sols 4804-4811, A. Fraeman, 2026-02-13",
        ],
    },
}