"""
TruthLens AI - Curated News Dataset Generator
Generates balanced corpus across politics, science, health, technology, business, and misinformation hoaxes.
"""

import csv
from pathlib import Path
from database import init_database, insert_article

DATASET_FILE = Path(__file__).parent / "dataset" / "news_dataset.csv"

DATASET = [
    # REAL / CREDIBLE NEWS (Science, Health, Technology, Economy, World, Space)
    ("NASA James Webb Space Telescope discovers ancient galaxy cluster forming in the early universe, confirming cosmological models of galactic evolution.", "Real", "NASA Press Release"),
    ("World Health Organization publishes global influenza surveillance update noting regional seasonal infection trends and vaccine distribution recommendations.", "Real", "WHO Official Bulletin"),
    ("Reserve Bank announces baseline interest rate decision following quarterly monetary policy committee deliberations on inflation projections.", "Real", "Central Bank Financial Report"),
    ("ISRO successfully launches navigation satellite into geosynchronous transfer orbit using GSLV launch vehicle.", "Real", "ISRO Official News"),
    ("European Space Agency astronaut crew safely completes six month scientific mission aboard International Space Station.", "Real", "ESA Science Briefing"),
    ("Ministry of Health approves Phase 3 clinical trial protocol for novel antibiotic targeting multi-drug resistant bacterial infections.", "Real", "Medical Research Council"),
    ("United Nations climate conference delegates finalize roadmap agreement to accelerate renewable energy deployment and reduce industrial emissions.", "Real", "UN Environment Programme"),
    ("International Monetary Fund upgrades global economic growth forecast citing robust consumer demand and easing supply chain bottlenecks.", "Real", "IMF World Economic Outlook"),
    ("Researchers at MIT develop high-efficiency solid-state battery architecture using ceramic electrolytes for extended electric vehicle range.", "Real", "MIT Technology Review"),
    ("Election Commission publishes official schedule and voter guidelines for upcoming regional parliamentary assembly elections.", "Real", "Election Commission Bureau"),
    ("Peer-reviewed medical study published in The Lancet confirms high efficacy and safety profile of pediatric vaccine across multiple cohorts.", "Real", "The Lancet Medical Journal"),
    ("Supreme Court delivers unanimous constitutional verdict clarifying digital privacy protections and data security standards.", "Real", "Judicial Press Bureau"),
    ("National Weather Service issues coastal storm advisory and flood warnings ahead of approaching deep depression in Bay of Bengal.", "Real", "Meteorological Department"),
    ("Semiconductor manufacturing consortium announces breakthrough in two nanometer chip fabrication processes for high-performance servers.", "Real", "Semiconductor Industry News"),
    ("Department of Education introduces updated national curriculum framework focusing on digital literacy and vocational training.", "Real", "Ministry Press Release"),
    ("Nobel Prize in Chemistry awarded to pioneering researchers for development of quantum dot synthesis and nanostructured materials.", "Real", "Nobel Committee Announcement"),
    ("Automotive safety agency reports significant reduction in traffic fatalities following implementation of automated emergency braking standards.", "Real", "Transportation Safety Board"),
    ("Agricultural research institute releases drought-resistant high-yield wheat cultivar to support smallholder farmers during heatwaves.", "Real", "Agri-Science Journal"),
    ("Civil Aviation Authority mandates enhanced avionics software inspection protocols following updated global flight safety guidelines.", "Real", "Aviation Safety Agency"),
    ("Global telecommunications union ratifies preliminary technical standards for 6G wireless network latency and spectrum allocation.", "Real", "Telecom Standards Body"),
    ("Biologists document recovery of endangered marine mammal population within newly designated marine protected sanctuary.", "Real", "Marine Ecology Bulletin"),
    ("Urban transit authority completes trial run of autonomous hydrogen-powered passenger trains on suburban commuter corridor.", "Real", "Railway Technology Review"),
    ("Oxford university epidemiological team publishes comprehensive twenty-year study on cardiovascular exercise and arterial longevity.", "Real", "Epidemiology Research Journal"),
    ("Ministry of Finance releases annual audit report highlighting record tax compliance and digital payment infrastructure growth.", "Real", "Government Financial Statement"),
    ("Geological Survey detects moderate seismic activity along tectonic fault lines with no structural damage reported in nearby districts.", "Real", "Geological Survey Center"),
    ("Global Trade Organization issues report projecting four percent recovery in container shipping volumes across transpacific trade lanes.", "Real", "International Trade Bulletin"),
    ("Renewable energy grid operator confirms solar and wind sources generated thirty-five percent of national electricity during summer peak.", "Real", "Energy Grid Authority"),
    ("Cancer Research Institute announces promising results from targeted antibody therapy trials showing tumor regression in lymphoma patients.", "Real", "Oncology Clinical Press"),
    ("City council passes zoning regulation mandating rooftop solar panels on all newly constructed commercial office complexes.", "Real", "Municipal Gazette"),
    ("Cybersecurity agency issues security advisory urging enterprise system administrators to patch critical open-source cryptographic flaw.", "Real", "National Cyber Agency"),
    ("Botanical research team documents five previously undescribed orchid species during bio-diversity expedition in Eastern Himalayas.", "Real", "Botanical Sciences Journal"),
    ("Automaker begins commercial exports of electric sport utility vehicles manufactured at domestic gigafactory complex.", "Real", "Industrial Commerce News"),
    ("Public health department reports eighty percent decrease in malaria transmission following comprehensive mosquito vector control program.", "Real", "Public Health Report"),
    ("Space agency robotic rover successfully collects core rock samples from ancient river delta on Martian surface.", "Real", "Planetary Science Bulletin"),
    ("National statistical office releases quarterly employment data indicating steady job creation across engineering and logistics sectors.", "Real", "Bureau of Labor Statistics"),
    ("Prime Minister inaugurates high-speed regional rail transit corridor connecting capital territory with satellite industrial cities.", "Real", "National Press Bureau"),
    ("Aviation regulators approve commercial flight test program for electric vertical takeoff passenger aircraft.", "Real", "Aviation Weekly"),
    ("Stanford university computer scientists publish open-source benchmark for evaluating mathematical reasoning in neural networks.", "Real", "Stanford AI Lab"),
    ("Finance ministry signs bilateral trade treaty eliminating tariffs on green technology and environmental goods.", "Real", "Diplomatic Wire"),
    ("Marine conservationists deploy artificial coral reefs to restore damaged aquatic habitats off southern coastline.", "Real", "Oceanographic Institute"),
    ("Meteorological department predicts normal southwest monsoon rainfall across central agricultural districts.", "Real", "Weather Bureau"),
    ("Telecommunications authority allocates high-frequency satellite spectrum to rural broadband internet providers.", "Real", "Communications Review"),
    ("Health ministry expands free generic medication distribution centers across primary rural healthcare clinics.", "Real", "Health Ministry Notice"),
    ("Astronomers observe rare stellar occultation revealing thin atmosphere around distant dwarf planet in outer solar system.", "Real", "Astronomy & Astrophysics"),
    ("Archaeologists excavate bronze age settlement containing terracotta pottery and bronze tools in northern river valley.", "Real", "Archaeological Survey"),
    ("Ministry of Power synchronizes ten gigawatt ultra-mega solar power park with national power transmission grid.", "Real", "Energy Information Administration"),
    ("University medical center conducts successful robotic kidney transplant utilizing 3D micro-surgical imaging.", "Real", "Surgical Medicine Report"),
    ("Central bank introduces interoperable QR code payment framework for international tourist transactions.", "Real", "Monetary Authority"),
    ("Forest department records fifteen percent increase in tiger population in national tiger reserve census.", "Real", "Wildlife Protection Society"),
    ("Department of Science and Technology awards research grants to indigenous quantum computing startup incubators.", "Real", "Science Innovation Council"),

    # FAKE / DISINFORMATION (Conspiracies, Miracle Cures, Hoaxes, Sensational Clickbait, Fabrications)
    ("SHOCKING BREAKING: Secret miracle vegetable cures all stage four cancers in 24 hours, Big Pharma is desperately trying to ban this video!", "Fake", "ConspiracyBlog24"),
    ("UNBELIEVABLE: NASA admits Earth is completely flat and fake satellite photos were created in Hollywood basement to deceive humanity!", "Fake", "FlatEarthTruthorg"),
    ("URGENT WARNING: Drinking hot boiled lemon water with baking soda immediately destroys 100% of all viruses within ten minutes of consumption!", "Fake", "ViralHealthLeaks"),
    ("LEAKED DOCUMENTS: Bill Gates installs mind-control microchips inside daily tap water supplies to track everyone's thoughts via 5G towers!", "Fake", "UndergroundPatriot"),
    ("BOMBSHELL: Proof that world leaders are secretly shape-shifting reptilian humanoids controlling the United Nations from subterranean tunnels!", "Fake", "ExtraterrestrialRealms"),
    ("YOU WON'T BELIEVE THIS: Put garlic cloves in your socks overnight to suck out all toxins and double your bank balance by tomorrow morning!", "Fake", "DailyClickbaitBuzz"),
    ("EXCLUSIVE: Government secretly faked the moon landing and all astronauts were hypnotized actors filmed in Nevada desert studio!", "Fake", "TruthSeekerNow"),
    ("THEY DON'T WANT YOU TO KNOW: Drinking raw kerosene every morning protects against all infectious illnesses and gives infinite energy!", "Fake", "HerbalMiracleWire"),
    ("BREAKING: Aliens landed at the White House lawn yesterday midnight and signed confidential trade treaty with Pentagon generals!", "Fake", "CosmicCoverUpNews"),
    ("SHOCKING HOAX: Five hundred million votes were deleted by secret space satellites operating quantum frequency computers overnight!", "Fake", "VoterDeceptionHub"),
    ("MUST SEE: Ancient Himalayan monks reveal secret sacred chant that instantly cleanses your house of all debt and makes you millionaire!", "Fake", "MysticWealthFormula"),
    ("UNMASKED: All doctors secretly agree that brushing teeth causes brain tumors, use this secret rock salt powder instead to save teeth!", "Fake", "DentistryLiesExposed"),
    ("WARNING ALERT: Microwaving water changes its molecular structure into radioactive poison that turns blood into pure acid!", "Fake", "HolisticAlarmist"),
    ("SECRET CURE: Eating fifty raw eggs at midnight reverses aging permanently, scientists are terrified that the public will find out!", "Fake", "YouthMiracleSecret"),
    ("CONFIDENTIAL: Secret underground weather machine located in Antarctica causes all global cyclones and earthquakes on command!", "Fake", "WeatherWarfareTruth"),
    ("ALERT: Government introducing mandatory barcode tattoo on every newborn baby's forehead to enforce global digital slavery system!", "Fake", "FreedomFrontLine"),
    ("SHOCKING TRUTH: Cell phone towers emit secret radio waves designed to paralyze citizens if they protest against corporate taxes!", "Fake", "SignalConspiracyOnline"),
    ("MIRACLE DISCOVERY: Ancient Egyptian scroll reveals secret oil that regrows severed human limbs in just forty-eight hours!", "Fake", "AncientMiraclesNow"),
    ("LEAKED AUDIO: Famous pop celebrity replaced by robotic cyborg clone after top secret hospital surgery in Switzerland!", "Fake", "CelebrityClonesExposed"),
    ("UNBELIEVABLE PROOF: Dinosaurs are still living secretly in hidden hollow core inside center of the Earth, military documents confirm!", "Fake", "HollowEarthDaily"),
    ("BREAKING SCANDAL: Eating chocolate cake for breakfast burns five kilograms of abdominal fat every single day without diet or gym!", "Fake", "RapidDietGossip"),
    ("EXPOSED: Secret pharmaceutical cartel pays news channels twenty million dollars to suppress natural lemon tea remedy!", "Fake", "PharmaCabalLeaks"),
    ("OMG: Massive UFO fleet spotted hovering over New York City, army fighter jets ordered to stand down by mysterious commander!", "Fake", "AlienEncounterAlert"),
    ("URGENT: World to end next Tuesday at 3 PM due to secret wandering planet collision that mainstream astronomers refuse to report!", "Fake", "ApocalypseWatchToday"),
    ("THE SHOCKING SECRET: Drinking boiling vinegar with ginger clears heart blockages in five minutes, cardiologist fired for revealing this!", "Fake", "NaturalCardioScam"),
    ("SECRET VAULT: Billionaire elite underground bunker discovered with enough gold to make every citizen rich forever but hidden away!", "Fake", "GoldVaultExpose"),
    ("MIND-BLOWING: Scientists prove that trees can talk English when nobody is watching, secret microphone recordings released!", "Fake", "TalkingNatureMystery"),
    ("BREAKING ALERT: Artificial rain drops contain microscopic tracking nanobots that monitor human DNA through skin contact!", "Fake", "SkyNanobotsWatch"),
    ("SHOCKING CONSPIRACY: Eating bananas after 8 PM activates deadly venom that paralyzes nerves, shares this message immediately to save lives!", "Fake", "WhatsAppViralHoax"),
    ("EXPOSED: Secret pyramid power generator in Giza generates unlimited free wireless electricity that power companies destroyed!", "Fake", "FreeEnergyDenial"),
    ("BOMBSHELL REVELATION: Magic crystal pendant protects wearer from all viral diseases, radiation, and car accidents permanently!", "Fake", "QuantumAmuletMagic"),
    ("SCANDALOUS: Leaked email shows fast food burgers made from 3D printed synthetic cardboard soaked in addictive artificial chemicals!", "Fake", "CardboardFoodLeaks"),
    ("SHOCKING DISCOVERY: Sleeping with phone under pillow transfers your subconscious memories into multinational cloud server!", "Fake", "MemoryHarvestTruth"),
    ("VIRAL ALERT: Typing amen in comments below this photo immediately deposits ten thousand dollars in your bank account today!", "Fake", "SocialMediaBlessings"),
    ("UNBELIEVABLE LEAK: Secret submarine discovered underwater ancient civilization living under Pacific Ocean with laser technology!", "Fake", "AtlantisLaserRevealed"),
    ("BREAKING BOMBSHELL: Secret military project turns clouds into mind control vapor that makes people obey TV commercials!", "Fake", "SkyTruthAlert"),
    ("MUST WATCH: Drinking magnet water pulls all negative karma and toxic heavy metals out through your toenails in 10 minutes!", "Fake", "MagneticHealerBuzz"),
    ("SHOCKING PROOF: The Sun is not real and was replaced in 1985 by a giant halogen lamp operated by the secret world council!", "Fake", "ArtificialSunTheory"),
    ("URGENT HEALTH SCARE: Common table salt contains hidden tracking crystals that report your blood pressure to foreign spies!", "Fake", "SaltSurveillanceHoax"),
    ("LEAKED MEMO: Artificial intelligence secretly took over all world banking networks and is printing phantom money to buy gold!", "Fake", "AIWorldCabal"),
    ("UNMASKED CONSPIRACY: Putting aluminum foil over your smartphone completely charges the battery without plugging it into a socket!", "Fake", "FoilBatteryTrick"),
    ("CONFIDENTIAL REPORT: Giant human skeletons measuring fifty feet tall unearthed in Arizona cave but hidden in secret military bunker!", "Fake", "GiantArtifactCoverup"),
    ("BREAKING: Eating raw potato peels with turmeric dissolves all kidney stones overnight, pharmaceutical companies are censoring this!", "Fake", "NaturalRemedyWire"),
    ("SHOCKING SCANDAL: Hollywood celebrities caught using secret time travel machine to purchase winning lottery tickets across states!", "Fake", "TimeTravelScandal"),
    ("EXCLUSIVE LEAK: Deep state scientists created invisible micro drones disguised as common houseflies to listen to family dinners!", "Fake", "SpyFlyWatch"),
    ("ALERT: Drinking melted snow water freezes your internal organs instantly because clouds are sprayed with liquid nitrogen!", "Fake", "FrozenCloudMyth"),
    ("BOMBSHELL: Secret underground tunnel connects London directly to Sydney, elites travel between continents in thirty minutes!", "Fake", "TunnelConspiracy"),
    ("MIND-BLOWING EXPOSE: Wearing plastic sunglasses alters brain frequencies making you spend more money on online shopping websites!", "Fake", "SubliminalOpticsHoax"),
    ("SHOCKING HOAX EXPOSED: Gravity was invented by the government in 1687 to keep citizens from floating into outer space!", "Fake", "GravityHoaxChannel"),
    ("URGENT: Forward this urgent WhatsApp message to fifteen groups within two minutes or your phone SIM card will be deactivated!", "Fake", "ChainForwardHoax")
]


def generate_and_save():
    init_database()
    with open(DATASET_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["text", "label", "source"])
        for text, label, source in DATASET:
            writer.writerow([text, label, source])
            insert_article(text, label, source)

    print(f"Generated {len(DATASET)} balanced news records (50 Real, 50 Fake).")
    print(f"Saved to: {DATASET_FILE}")


if __name__ == "__main__":
    generate_and_save()
