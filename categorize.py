from openai import OpenAI

# Define categories and sub-categories
categories = {
    "HomeDecore": ["Construction", "Decore DIY", "Furniture/ WoodWorking", "Home / house Tour", "Home Renovation",
                   "Interior design", "Paint / Wall Painting / Putty / Distemper/ Wallpaper", "Home Furnishing",
                   "Home Improvement Tool", "Home Cleaning", "Home Design Maps", "Home Security", "Smart Home",
                   "Pest control", "Home Electric", "Lawn Mower", "Home Organize", "Civil Engineering", "WoodCutting",
                   "Heavy Machinery", "Environmental Safety"],
    "BusinessFinance": ["Bitcoin", "Investment", "Mutual Fund", "Investor", "Stock Market", "Blockchain/Crypto",
                        "Banking", "Insurance", "Ethereum", "Business idea", "Loan", "Financial Advisor",
                        "Industrial Talks", "Shipping and logistics", "Payment/bank apps", "Currency", "Taxation",
                        "Informative/GA", "Online Earn Jobs", "Metals Industry", "Workshop/Manufacturing Industry"],
    "FoodBeverage": ["Cooking/Recipe", "Eating", "shakes/Smoothies", "Food reviews", "Baking", "Kitchen",
                     "Tea/Coffee", "Ice Cream", "Non-alcoholic Cocktail/Drinks", "QSR", "Barbecues and Grilling"],
    "HomeAppliance": ["Kitchen Products", "TV", "Washing Machine", "Oven", "Fridge", "AC", "Air Purifire",
                      "Vaccum Cleaner", "Stove", "Utensils", "Home Theater", "ceiling fan", "Water Purifier",
                      "Consumer Electronics", "Consumer Electronics Repair", "Water Heater"],
    "HouseholdSupplies": ["Soap", "Washing Powder", "Disinfectant", "Laundry"],
    "Automobile": ["Car & Reviews", "Bike & Reviews", "Car Repair", "Bike Repair", "Utility Vehicles", "Cycle",
                   "Commercial Vehicles", "Car Parts Content", "Bike Parts Content", "EV Cars Repair", "EV Cars Review",
                   "EV Bike Repair", "EV Bike Review", "Car Driving", "Bike Riding", "Car Stereo System", "Aircraft",
                   "Construction Vehicle", "Car & Bike", "Car Modification", "Bike Modification", "Truck",
                   "Engine Oil/Lubricant",
                   "Car Wash", "Bike Wash", "All type of Vehicles", "3 Wheeler & Review", "3 Wheeler Repair",
                   "Bike Ride Gears",
                   "Engine"],
    "AgricultureFarming": ["Outdoor Gardening", "Indoor Gardening", "Farming Vehicle Tractor", "Agriculture",
                           "Soil in Agriculture", "Seed", "Rice paddy", "Fish Farming", "Dairy Farming",
                           "Goat & Sheep Farming",
                           "Poultry Farming", "Plantation Farming", "Agriculture information",
                           "Agriculture organization",
                           "Pig Farming", "Solar Equipments", "Vegetable/Fruit Market Price"],
    "Kids": ["Cartoon/Animation", "13+ Cartoon/Content", "Toys/Unboxing", "Parenting", "Baby products",
             "Nursery Rhymes",
             "Kids Content", "Stories", "Baby/kids prank/Funny/vines", "Art & DIY", "Drawing", "Kid/baby Food",
             "Kids Reality TV Shows", "Slime relax video", "Kids/Baby Education", "Lullaby"],
    "Alcohol": ["Beer", "Vodka", "Whiskey", "Rum", "Brandy", "Wine", "Beer Brew Tool", "All type of alcohol", "Bar",
                "Bartender"],
    "Education": ["Online Eductaion", "School", "foreign/language learning", "University/College", "Computer Languages",
                  "Homeschooling", "Special Education", "Science", "Mathematics", "Competitive exams", "Data science",
                  "Artificial intelligence", "Game development tutorial", "Business Education", "Law Education",
                  "Economics", "Study Tips", "Stationery", "Informative/GA", "Engineering", "Digital Marketing"],
    "CareerJobs": ["Job Search", "Job Fairs", "Resume Writing/Advice", "Career Advice", "Career Planning", "Govt Jobs"],
    "Dental": ["Oral Care", "Dentist", "Dental", "Toothpaste", "Toothbrush", "Denture", "Floss"],
    "HealthWellness": ["Wellness", "Nutrition videos", "Pediatrics", "Women's Health", "Men's Health", "Home Remedies",
                       "Osteopathy (medical)", "Massage", "Meditation", "Medical Guide & info", "Health Advice & Tips",
                       "Eye Care", "Medical Education", "Hospital", "Mental Health", "Disease Tips & info",
                       "About Medicine",
                       "Medical tools", "Pharmacy Apps"],
    "Movie": ["Full Movies(All type)", "Trailers", "Movie Review", "Movie Reaction", "Romantic Movie",
              "Action-Advanture",
              "Drama", "Horror Movie", "Documentary Movie", "Movie Clip", "Comedy Movie"],
    "Entertainment": ["Web Series", "Tv Serial / Tv Show", "Behind The Scene / Bloopers", "Production house", "Comedy",
                      "Yt Short Films", "Books & Comics", "Events", "Performing Arts", "Lifestyle Vlog", "Family Vlog",
                      "Info Entertainment", "Award Show", "Prank/Vines/memes", "Reaction Video", "Tv Channel",
                      "Podcast",
                      "Celeb News", "Dance", "Voice Artist", "Experimental", "Radio/FM", "Culture", "Dating", "Actor",
                      "Actress", "Magzine", "Superhero", "Internet celebrity", "Lyrics_Storytelling", "ASMR"],
    "StyleFashion": ["Fashion Haul", "Shoes & Footwear", "Jewellery", "Fashion Accessories", "Fashion Show",
                     "Bikni Haul",
                     "Men Grooming", "Fashion DIY", "Beauty Pageants", "Designer fashion", "Fashion Magazine",
                     "Fashion Academy",
                     "Ethnic Haul"],
    "Fitness": ["Yoga", "Home Workout", "Gym/Crossfit", "Zumba", "Cardio", "Running", "Outdoor exercise",
                "Healthy Food",
                "Fitness and Exercise info", "Bodybuilding Show", "Fitness Podcast", "Active wear"],
    "Travel": ["Camping", "Safari/Wildlife", "Visa (Education apply)", "Hiking/Trekking", "Parks (theme & Amusement)",
               "Hotel & Resorts", "Travel Vlog", "tourist Place", "Motor Vlogging", "travel agencie",
               "public transport",
               "Historic Places", "Fishing", "Travel Preparation and Advice", "Travel Equipment", "Cruize", "Beaches",
               "Ocean",
               "Mountain", "Sailing", "Boat", "Nightlife", "Biking/quad bikes", "Campervan/Vanlife", "Archaeologist",
               "Museum"],
    "ScienceTechnology": ["Astronomy", "Computer Science", "Earth Sciences", "Ecology & Environment",
                          "Scientific Equipment",
                          "Computer Networking", "Computer Peripherals", "Computer Software and Applications",
                          "Data Storage and Warehousing", "Information and Network Security", "Robotics", "Telecom",
                          "Apps Info"],
    "Gadget": ["Gadget Reviews", "Smartphones", "Computer/laptop", "Home Entertainment Systems", "Wearable Technology",
               "Cameras and Camcorders", "Tablets and E-readers", "AR and VR", "Drone", "Mobile Repair"],
    "Music": ["Concert/Live Show", "Singing", "Musical instrument", "Soundtracks, TV and Showtunes", "Music videos",
              "Classical Music", "Country Music", "Hip Hop Music", "Jazz", "R&B/Soul/Funk", "Rock Music",
              "Songwriters/Folk",
              "Music/Group/Band Official", "Radio/FM", "Musical Artist Official", "beatbox",
              "Lyric/SingleFrame/Long Music/Playlist",
              "Relaxation Music", "Musical Electronic Equipment"],
    "Sports": ["Baseball", "Basketball", "Football", "Cricket", "Golf", "Tennis", "Ice Hockey", "Volleyball",
               "American Football",
               "Rugby", "Boxing", "Wrestling", "Mixed Martial Arts", "Swimming", "Diving", "Water Polo", "Canoeing",
               "Rowing",
               "Badminton", "Squash", "Table Tennis", "Athletics", "Cycling", "Gymnastics", "Triathlon",
               "Animal Sports",
               "Motor Sports", "Sport Scores & Statistics", "Sporting Goods", "Sports Coaching & Training",
               "Sports Gear & Apparel",
               "Sports review", "Hockey", "Running/Marathon", "All types of sports activity", "Arm Wrestling",
               "Sport Betting",
               "Pool/Billiards/Snooker", "Archery", "Golf Disc", "Sports News", "Kabaddi", "Lacrosse", "Stadium",
               "Other Sports"],
    "ExtermeSports": ["Scuba Diving", "Wakeboarding", "Kitesurfing", "Parasailing", "Barefoot Skiing", "Kayaking",
                      "Windsurfing",
                      "Surfing", "Freediving", "Rafting", "Skateboarding", "Sandboarding", "Caving", "Parkour",
                      "Climbing",
                      "Paragliding", "Skydiving", "Bungee Jumping", "Zip-lining", "BMX racing", "Mountain Biking",
                      "Motocross",
                      "MonsterTruck", "Skiing", "All type of exterme sports", "Snowboarding",
                      "Extreme Sports Gear & Apparel", "Skating"],
    "PetAnimal": ["Cat", "Dog", "Bird", "Fish", "Turtle", "Rabbit", "Snake", "Lizard", "Pet Food", "Pet Accessories",
                  "Animal Products & Services", "Aquariums", "Veterinary Medicine", "Wildlife animals", "Spider",
                  "Elephant",
                  "All Type of Animal", "Monkey", "Rodent", "Fox", "Reptiles", "Horse", "Zoo", "Pig", "Squirrel",
                  "Otter", "Racoon",
                  "Pet Show", "Marine Mammal", "Bear", "Fennec Fox", "Highland cattle", "Cat & Dog", "Animal Rescue",
                  "Cow", "Veterinarian"],
    "Gaming": ["Arcade & Coin-Op Games", "Board Games", "Card Games", "Dice Games", "E-sports games",
               "Shooting(FPS) Games",
               "Mobile Games", "Gaming Peripherals", "Fight Games", "Sports Games", "Racing Games", "Action-adventure",
               "Gaming Consoles", "All type of Video Games", "Game Review/Comparison", "Horror Games",
               "Gaming Animation"],
    "RealEstate": ["Property Development", "Real Estate Listings", "Real Estate Services", "Real Estate Buy/Sell/Rent"],
    "Shopping": ["Antiques & Collectibles", "Auctions", "Discount & Outlet Stores", "Gifts & Special Event Items",
                 "Green & Eco-Friendly Shopping", "Mass Merchants & Department Stores", "Shopping Portals",
                 "Swap Meets & Outdoor Markets",
                 "Wholesalers & Liquidators", "Grocery Shopping"],
    "ArtCraft": ["Digital art (Photography, videography, any form of digitally created art)", "Visual Art & Design",
                 "DIY craft",
                 "Life hacks", "Megnet DIY", "Tech DIY", "Tools DIY", "Drawing", "Body Art", "3D Printing and Device"],
    "Beauty": ["Makeup", "Hair Care", "Skin Care", "Skin/Hair (Health) Care remedy", "Nail Care",
               "Beauty Services & Spas",
               "Perfume and Deodorant", "Skin/Hair Remedies", "Cosmetology & Beauty Professionals"],
    "Motivation": [],
}
max = ""
for x in categories.values():
    for y in x:
        if len(y) > len(max):
            max = y
print(max)
def ask_gpt( title, description, titels, cat=1):
    z = 0
    if cat == 1:
        l = categories.keys()
        sub = False
    else:
        l = categories[cat]
        sub = True
    while True:
        chat = f"""Channel Name: {title}
                           Channel Description: {description}
                           Video Titles: {titels}"""

        # Initialize OpenAI client
        client = OpenAI(api_key='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')
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": f"You have to tell in which category from the given list the channel lies.{l} on the basis of contend they deliver. Only return the category exactly same as in the list. No extra word."},
                {"role": "user", "content": chat}
            ],
            max_tokens=16
        )
        result = str(completion.choices[0].message.content)



        if sub and result in categories[cat]:
            return result
        elif result in categories.keys():
            return result

        z += 1

        if z == 10:
            print('Error')
            return None
