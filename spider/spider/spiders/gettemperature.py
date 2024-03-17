# crawl temperature spider
# new terminal, cd spider
# scrapy crawl temperature_data -o temperature_data.jl

import scrapy

class TemperatureSpider(scrapy.Spider):
    name = 'temperature_data'
    start_urls = ['https://data.giss.nasa.gov/gistemp/graphs/graph_data/Global_Mean_Estimates_based_on_Land_and_Ocean_Data/graph.txt']

    def parse(self, response):
        lines = response.text.split('\n')
        data_lines = lines[5:]

        for line in data_lines:
            if line.strip():
                parts = line.split()
                # Extract year, no smoothing, and Lowess(5) values
                if len(parts) >= 3:
                    year = parts[0]
                    no_smoothing = parts[1]
                    lowess_5 = parts[2]
                    yield {
                        'year': year,
                        'no_smoothing': no_smoothing,
                        'lowess_5': lowess_5
                    }
