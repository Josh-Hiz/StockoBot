def parse_json(data):
    """
    Parses AlphaVantage JSON to get the following:
    - Symbol
    - Open
    - High
    - Low
    - Price
    - Volume
    - Latest Trading Day
    - Previous Close
    - Change
    - Change Percent
    """
    return {"open":data["Global Quote"]["02. open"],
            "high":data["Global Quote"]["03. high"],
            "low":data["Global Quote"]["04. low"],
            "price":data["Global Quote"]["05. price"],
            "volume":data["Global Quote"]["06. volume"],
            "ltd":data["Global Quote"]["07. latest trading day"],
            "change":data["Global Quote"]["09. change"],
            "change percent":data["Global Quote"]["10. change percent"]}
        

