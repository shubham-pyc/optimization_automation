
# OBJECTS RELATED TO ELIGIBILITY CRITERIA

IS_SINGLE_PAX = {
    "requirement":"Bootstrapper.dataObject.page.flightSearch",
    "call":"isSinglePax()",
    "code":"""// Validate for single Pax
function isSinglePax() {
    var flag = false;
    try {
        // Pax count already checked in Parent method "runVariant" 
        var paxCount = Bootstrapper.dataObject.page.flightSearch.paxCount;
        if (paxCount == 1) {
            flag = true;
        } else {
            DL_OBJ.EXCLUDE_REASON = "excludeIneligible|Pax count "+ paxCount;
        }
    } catch (e) {
        var msg = "exception occur while rendering isSinglePax method",
            method = 'isSinglePax',
            input = {
                "error_message": e.message,
                "error_name": e.name
            };
        DL_OBJ.dataGapHandler(msg, method, input);
    }
    return flag;
}
"""
}

IS_USER_LOGIN = {
    "requirement":"UA.AppData.Data.Session",
    "call":"isUserLogin()",
    "code":"""//Function to check if the user is login
function isUserLogin(){
    var retValue = false;
    try{
        retValue = UA.AppData.Data.Session.IsSignedIn;
    } catch(e){
        var msg = 'Exception occured in running isUserLogin method',
            method= 'isUserLogin',
            input = {
                "error_message":e.message,
                "error_name":e.name,
            };
        DL_OBJ.dataGapHandler(msg, method, input);
    }
    return retValue;
}

"""
}

IS_ROUND_TRIP = {
    "requirement":"UA.AppData.Data.Search",
    "call":"isTripTypeRoundTrip()",
    "code":"""//Function to check if round trip selected
function isTripTypeRoundTrip() {
    var flag = false;
    try {
        var tripType = UA.AppData.Data.Search.SearchMethod;
        if (tripType == 'roundTrip') {
            flag = true;
        } else {
            DL_OBJ.EXCLUDE_REASON = "excludeIneligible|search type "+ tripType;
        }
    } catch (e) {
        var msg = "exception occur while rendering isTripTypeRoundTrip method",
            method = 'isTripTypeRoundTrip',
            input = {
                "error_message": e.message,
                "error_name": e.name
            };
        DL_OBJ.dataGapHandler(msg, method, input);
    }
    return flag;
}

"""
}

IS_DOMESTIC_SEARCH = {
    "requirement":"UA.AppData.Data.Search",
    "call":"isDomestic()",
    "code":"""function isDomesticSearch() {
    var isDomestic = false,
        countryType = '';
    try {
        // countryType = (UA.AppData.Data.Search.SearchMethod == 'multiCity') ? "Domestic" : getMarketType();
       
        countryType = (UA.AppData.Data.Search.SearchMethod == 'multiCity') ? false : getMarketType();

        if (countryType == "Domestic") {
            isDomestic = true;
        } else {
            var label = "excludeIneligible|International search";
            window.ga(DL_OBJ.GA_METHOD, DL_OBJ.GA_EVENT, DL_OBJ.GA_CATEGORY,  DL_OBJ.CAMPAIGN_NAME, label);
        }
    } catch (e) {
        var msg = "exception occur while checking for domestic searches",
        method = 'isDomesticSearch',
        input = {
            "error_message": e.message,
            "error_name": e.name
        };
        DL_OBJ.dataGapHandler(msg, method, input);
    }
    return isDomestic;
}

function getMarketType(){
    var marketType = "--";
    var methodName = "getMarketType";
    try{        
        var tripObject = (Bootstrapper.dataObject.getData("Trips", "srchRslts", "page") && Bootstrapper.dataObject.getData("Trips", "srchRslts", "page").length) ? Bootstrapper.dataObject.getData("Trips", "srchRslts", "page")[0] : "";
        if(tripObject){
            marketType = Bootstrapper.processMarketTypeValue(tripObject);
        }
    } catch (e) {
        var msg = "exception occur while fetching get market type",
        method = 'getMarketType',
        input = {
            "error_message": e.message,
            "error_name": e.name
        };
        DL_OBJ.dataGapHandler(msg, method, input);
    }
    return marketType;
}

"""
}


CRITERIA_CODE_MAPPING = {
        "roundtrip":IS_ROUND_TRIP,
        "singlepax":IS_SINGLE_PAX,
        "userlogin":IS_USER_LOGIN,
        "domesticflight":IS_DOMESTIC_SEARCH
}