import scrapy
import json
import re


class ProfilesSpider(scrapy.Spider):
    name = "profiles"
    start_urls = [
        "https://www.worldsurfleague.com/athletes/tour/mct?year=2010",
        "https://www.worldsurfleague.com/athletes/tour/mct?year=2011",
        "https://www.worldsurfleague.com/athletes/tour/mct?year=2012",
        "https://www.worldsurfleague.com/athletes/tour/mct?year=2013",
        "https://www.worldsurfleague.com/athletes/tour/mct?year=2014",
        "https://www.worldsurfleague.com/athletes/tour/mct?year=2015",
        "https://www.worldsurfleague.com/athletes/tour/mct?year=2016",
        "https://www.worldsurfleague.com/athletes/tour/mct?year=2017",
        "https://www.worldsurfleague.com/athletes/tour/mct?year=2018",
        "https://www.worldsurfleague.com/athletes/tour/mct?year=2019",
        "https://www.worldsurfleague.com/athletes/tour/mct?year=2020",
        "https://www.worldsurfleague.com/athletes/tour/mct?year=2021",
        "https://www.worldsurfleague.com/athletes/tour/mct?year=2022",
        "https://www.worldsurfleague.com/athletes/tour/mct?year=2023",
        "https://www.worldsurfleague.com/athletes/tour/wct?year=2024",
        "https://www.worldsurfleague.com/athletes/tour/wct?year=2010",
        "https://www.worldsurfleague.com/athletes/tour/wct?year=2011",
        "https://www.worldsurfleague.com/athletes/tour/wct?year=2012",
        "https://www.worldsurfleague.com/athletes/tour/wct?year=2013",
        "https://www.worldsurfleague.com/athletes/tour/wct?year=2014",
        "https://www.worldsurfleague.com/athletes/tour/wct?year=2015",
        "https://www.worldsurfleague.com/athletes/tour/wct?year=2016",
        "https://www.worldsurfleague.com/athletes/tour/wct?year=2017",
        "https://www.worldsurfleague.com/athletes/tour/wct?year=2018",
        "https://www.worldsurfleague.com/athletes/tour/wct?year=2019",
        "https://www.worldsurfleague.com/athletes/tour/wct?year=2020",
        "https://www.worldsurfleague.com/athletes/tour/wct?year=2021",
        "https://www.worldsurfleague.com/athletes/tour/wct?year=2022",
        "https://www.worldsurfleague.com/athletes/tour/wct?year=2023",
        "https://www.worldsurfleague.com/athletes/tour/wct?year=2024",
    ]

    def start_requests(self):
        return super().start_requests()

    def parse(self, response):
        for link in response.xpath(
            '//table//a[contains(@class, "athlete-name")]/@href'
        ):  # css to href to their profile:
            yield response.follow(link.get(), callback=self.parse_profile)

    def parse_profile(self, response):
        # follow links to profile and collect data on surfer age, hometown, height, weight
        # TODO: fix stance
        surfer_name = (
            response.css(".avatar-text-primary > h1::text").extract_first().strip()
        )  # css to name
        surfer_country = response.css(".country-name::text").extract_first().strip()
        followers = response.css(".count::text").extract_first().strip()
        surfer_stance = surfer_stance = response.css(
            ".new-athlete-bio-stats > ul > li:nth-of-type(1) > div:nth-of-type(2)::text"
        ).extract()
        surfer_first_season = response.css(
            ".new-athlete-bio-stats > ul > li:nth-of-type(2) > div:nth-of-type(2)::text"
        ).extract()
        surfer_age = response.css(
            ".new-athlete-bio-stats > ul > li:nth-of-type(3) > .value > span:nth-of-type(1)::text"
        ).extract()
        surfer_bday = response.css(
            ".new-athlete-bio-stats > ul > li:nth-of-type(3) > .value > span:nth-of-type(2)::text"
        ).extract()
        surfer_height = response.css(
            ".new-athlete-bio-stats > ul > li:nth-of-type(4) > div:nth-of-type(2) > span:nth-of-type(2)::text"
        ).extract()
        surfer_weight = response.css(
            ".new-athlete-bio-stats > ul > li:nth-of-type(5) > div:nth-of-type(2) > span:nth-of-type(2)::text"
        ).extract()
        surfer_hometown = response.css(
            ".new-athlete-bio-stats > ul > li:nth-of-type(6) > div:nth-of-type(2)::text"
        ).extract()
        profile_data = {
            "Name": surfer_name,
            "Nation": surfer_country,
            "Followers": followers,
            "Age": surfer_age,
            "Birthdate": surfer_bday,
            "Height": surfer_height,
            "Weight": surfer_weight,
            "Hometown": surfer_hometown,
            "First Season": surfer_first_season,
            "Stance": surfer_stance,
        }
        with open(f"profiles_{re.sub(r"https://www.worldsurfleague.com/athletes/\d+/", "", response.url)}.json", "w") as file:
            json.dump(profile_data, file)
        yield profile_data
