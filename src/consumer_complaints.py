import sys
import csv
from collections import OrderedDict, defaultdict

class ConsumerComplaints(object):
    """
    Implements the core modules to subset and
    parse the consumer complaints data file and produce the desired
    output file
    """
    def __init__(self, input_file, output_file):
        """
        Initializes object of a class
        :param input_file: a csv file that contains the consumer complaints data
        :param output_file: a csv file with four ouput columns including product, year, total
        complaints, total companies that received complaints, and the highest percentage of
        complaints filed towards one company
        """
        self.inputfile = input_file
        self.outputfile = output_file
        self.datalist = []
        self.rawdict = defaultdict(lambda : defaultdict(lambda : defaultdict(int)))
        self.aggdict = defaultdict(lambda : defaultdict(dict))
        self.sorteddict = OrderedDict()
        self.outputlist = []


    def get_columns(self):
        """
        Gets data from the required columns from the input file
        and stores them to a list of list
        """
        with open(self.inputfile) as csvfile:
            read_csv = csv.reader(csvfile, delimiter = ',')
            next(read_csv)
            for row in read_csv:
                try:
                    year = row[0][0:4] #Keeps the first four digits in date_created column
                    product = row[1].lower() #Extracts product name
                    company = row[7].lower() #Extracts company name
                    row_list = [year, product, company]
                    self.datalist.append(row_list)
                except Exception as e:
                    pass


    def parse_list(self):
        """
        Parse a list of data into a nested dictionary with three keys
        """
        for row in self.datalist:
            try:
                product = row[1]
                year = row[0]
                company = row[2]
                self.rawdict[product][year][company] += 1
            except Exception as e:
                pass


    def aggregate_dict(self):
        """
        Aggregate values from Company key to compute the desired values,
        including total complaints, total companies,
        and max percentage for each pair of product and year
        """
        for product in self.rawdict:
            for year in self.rawdict[product]:
                try:
                    total_complaints = sum(self.rawdict[product][year].values()) #Sum of company counts to get total complaints received
                    self.aggdict[product][year]['Total Complaints'] = total_complaints

                    total_companies = len(set(self.rawdict[product][year].keys())) #Total number of unique companies that received at least one complaint
                    self.aggdict[product][year]['Total Companies'] = total_companies

                    max_perc = round(max(self.rawdict[product][year].values()) / total_complaints * 100) #Highest percentage of complaints received by one single company
                    self.aggdict[product][year]['max percent'] = max_perc
                except Exception as e:
                    pass


    def sort_dict(self):
        """
        Sorts a dictionary by the product and year keys
        """
        try:
            ##changes made here#
            for product in self.aggdict:
                self.aggdict[product] = OrderedDict(sorted(self.aggdict[product].items())) #Sorts inner dictionary by year
            ##changes end here
            self.sorteddict = OrderedDict(sorted(self.aggdict.items())) #Sorts dictionary by product
        except Exception as e:
            pass


    def dict_to_list(self):
        """
        Converts a nested dictionary back to a flat list with four output elements
        and stores them in an output list
        """
        for product in self.sorteddict:
            for year in self.sorteddict[product]:
                try:
                    product_reformat = (lambda product:'"' + product.strip('"') + '"' if "," in product else product.strip('"'))(product) #Adds double quotation marks to a product name containing comma
                    key_list = [product_reformat,int(year)]
                    answer_list = [items for items in self.sorteddict[product][year].values()]
                    concat_list = key_list + answer_list
                    self.outputlist.append(concat_list)
                except Exception as e:
                    pass


    def write_output(self):
        """
        Writes the outputlist to a csv file
        """
        with open(self.outputfile, 'w') as csv_w_file:
            writer = csv.writer(csv_w_file)
            writer.writerows(self.outputlist)


    def main(self):
        self.get_columns()
        self.parse_list()
        self.aggregate_dict()
        self.sort_dict()
        self.dict_to_list()
        self.write_output()


if __name__ == "__main__":
    obj1 = ConsumerComplaints(sys.argv[1], sys.argv[2])
    obj1.main()
