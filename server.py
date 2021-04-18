from flask import Flask, render_template
import requests
import os

NASA_API_KEY = os.environ.get("NASA_API_KEY")
ENDPOINT = "https://api.nasa.gov/planetary/apod"

app = Flask(__name__)

planets = {
    "MERCURY": {
        "img": "https://images-assets.nasa.gov/image/PIA15164/PIA15164~orig.jpg",
        "explanation": "Mercury is the smallest and closest planet to the Sun in the Solar System. Its orbit around the Sun takes 87.97 Earth days, the shortest of all the planets in the Solar System. It is named after the Roman god Mercurius (Mercury), god of commerce, messenger of the gods, and mediator between gods and mortals, corresponding to the Greek god Hermes (Ἑρμῆς).",
        "date": "2011-12-02"
    },
    "VENUS": {
        "img": "https://images-assets.nasa.gov/image/GSFC_20171208_Archive_e001732/GSFC_20171208_Archive_e"
               "001732~orig.jpg",
        "explanation": "NASA image captured June 6, 2012. On June 5-6 2012, SDO is collecting images of one of the "
                       "rarest predictable solar events: the transit of Venus across the face of the sun. This event "
                       "happens in pairs eight years apart that are separated from each other by 105 or 121 years. "
                       "The last transit was in 2004 and the next will not happen until 2117.",
        "date": "2017-12-07"
    },
    "EARTH": {
        "img": "https://images-assets.nasa.gov/image/PIA18033/PIA18033~orig.jpg",
        "explanation": "Behold one of the more detailed images of the Earth yet created. This Blue Marble Earth montage"
                       " shown above -- created from photographs taken by the Visible/Infrared Imager Radiometer Suite "
                       "(VIIRS) instrument on board the new Suomi NPP satellite -- shows many stunning details of our"
                       " home planet. The Suomi NPP satellite was launched last October and renamed last week after "
                       "Verner Suomi, commonly deemed the father of satellite meteorology. The composite was created "
                       "from the data collected during four orbits of the robotic satellite taken earlier this month "
                       "and digitally projected onto the globe. Many features of North America and the Western "
                       "Hemisphere are particularly visible on a high resolution version of the image.",
        "date": "2012-01-30"
    },
    "MARS": {
        "img": "https://images-assets.nasa.gov/image/PIA04591/PIA04591~orig.jpg",
        "explanation": "Mars is the fourth planet from the Sun and the second-smallest planet in the Solar System, being larger than only Mercury. In English, Mars carries the name of the Roman god of war and is often referred to as the 'Red Planet'.[16][17] The latter refers to the effect of the iron oxide prevalent on Mars's surface, which gives it a reddish appearance distinctive among the astronomical bodies visible to the naked eye.[18] Mars is a terrestrial planet with a thin atmosphere, with surface features reminiscent of the impact craters of the Moon and the valleys, deserts and polar ice caps of Earth.",
        "date": "2003-06-25"
    },
    "JUPITER": {
        "img": "https://images-assets.nasa.gov/image/hubble-captures-vivid-auroras-in-jupiters-atmosphere_28"
               "000029525_o/"
               "hubble-captures-vivid-auroras-in-jupiters-atmosphere_28000029525_o~orig.jpg",
        "explanation": "Astronomers are using the NASA/ESA Hubble Space Telescope to study auroras — stunning light "
                       "shows in a planet’s atmosphere — on the poles of the largest planet in the solar system, "
                       "Jupiter. This observation program is supported by measurements made by NASA’s Juno spacecraft, "
                       "currently on its way to Jupiter. Jupiter, the largest planet in the solar system, is best"
                       " known for its colorful storms, the most famous being the Great Red Spot. Now astronomers "
                       "have focused on another beautiful feature of the planet, using Hubble's ultraviolet "
                       "capabilities. The extraordinary vivid glows shown in the new observations are known "
                       "as auroras. They are created when high-energy particles enter a planet’s atmosphere near"
                       " its magnetic poles and collide with atoms of gas.",
        "date": "2016-06-30"
    },
    "SATURN": {
        "img": "https://images-assets.nasa.gov/image/PIA04913/PIA04913~orig.jpg",
        "explanation": "Saturn is the sixth planet from the Sun and the second-largest in the Solar System, after Jupiter. It is a gas giant with an average radius of about nine times that of Earth. It only has one-eighth the average density of Earth; however, with its larger volume, Saturn is over 95 times more massive. Saturn is named after the Roman god of wealth and agriculture; its astronomical symbol (♄) represents the god's sickle. The Romans named the seventh day of the week Saturday, Sāturni diēs ('Saturn's Day') no later than the 2nd century for the planet Saturn.",
        "date": "2003-12-05",

    },
    "URANUS": {
        "img": "https://images-assets.nasa.gov/image/stsci-h-p1906c-f-514x514.a/stsci-h-p1906c-f-514x514.a~orig.png",
        "explanation": "This Hubble Space Telescope Wide Field Camera 3 image of Uranus, taken in November 2018,"
                       " reveals a vast, bright stormy cloud cap across the planet's north pole.",
        "date": "2019-02-11"
    },
    "NEPTUNE": {
        "img": "https://images-assets.nasa.gov/image/PIA01492/PIA01492~orig.jpg",
        "explanation": "This picture of Neptune was produced from the last whole planet images taken through the "
                       "green and orange filters on NASA's Voyager 2 narrow angle camera. The images were taken at a "
                       "range of 4.4 million miles from the planet, 4 days and 20 hours before closest approach. "
                       "The picture shows the Great Dark Spot and its companion bright smudge; on the west limb the "
                       "fast moving bright feature called Scooter and the little dark spot are visible. These clouds "
                       "were seen to persist for as long as Voyager's cameras could resolve them. North of these, "
                       "a bright cloud band similar to the south polar streak may be seen.",
        "date": "1998-10-30"
    }

}

first_img = {
    "img": "https://apod.nasa.gov/apod/image/0510/allskymilkyway_brunier.jpg",
    "explanation": "The disk of our Milky Way Galaxy is home to hot nebulae, cold dust, and billions of stars. "
                   "This disk can be seen from a dark location on Earth as a band of diffuse light across the sky. "
                   "This band crosses the sky in dramatic fashion in the above series of wide angle sky exposures "
                   "from Chile. The deepness of the exposures also brings to light a vast network of complex dust "
                   "filaments. Dust is so plentiful that it obscures our Galaxy's center in visible light, hiding"
                   " its true direction until discovered by other means early last century. The Galactic Center, "
                   "though, is visible above as the thickest part of the disk. The diffuse glow comes from billions "
                   "of older, fainter stars like our Sun, which are typically much older than the dust or any of "
                   "the nebulae. One particularly photogenic area of darkness is the Pipe Nebula visible above the"
                   " Galactic Center. Dark dust is not the dark matter than dominates our Galaxy -- that dark matter"
                   " remains in a form yet unknown.",
    "date": "2005-10-04"

}
# The data above is taken from NASA documents.


@app.route("/")
def home():
    return render_template("index.html", planets=planets, random=first_img)


@app.route("/random_image", methods=["POST"])
def fetch_random_image():
    parameters = {
        "count": 1,
        "thumbs": True,
        "api_key": NASA_API_KEY
    }
    response = requests.get("https://api.nasa.gov/planetary/apod", params=parameters)
    response.raise_for_status()
    data = response.json()
    random_img = {
        "img": data[0]["url"],
        "explanation": data[0]["explanation"],
        "date": data[0]["date"]
    }
    return render_template("index.html", random=random_img, planets=planets)


if __name__ == "__main__":
    app.run(debug=True)
