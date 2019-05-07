COMMON_CODE = """Bootstrapper._BkPth$replace = {
    CAMPAIGN_NAME: "QA - BookingPath_$campaign",
    VIRTUALPAGE: "D2.0 - - Stage",
    INCLUDE: false,
    CAMPAIGNREQUESTED: false,
    GA_METHOD: "send",
    GA_EVENT: "event",
    GA_CATEGORY: "Maxymiser PC",
    GA_EXCEPTION_CATEGORY: "DataGapTracking",
    GA_EXCEPTION_ACTION: "WebOptimization",
    EXCLUDE_REASON: ''
};

// Adding Datagap Handler Obj
Bootstrapper._BkPth$replace.dataGapHandler = function(message, method_name, additional_info) {
    var dateObj = new Date(),
        current_timestamp = dateObj.getTime(),
        customLabel = {
            "campaign": Bootstrapper._BkPth$replace.CAMPAIGN_NAME,
            "message": message,
            "method_name": method_name,
            "additional_info": additional_info,
            "time_stamp": current_timestamp
        };
    window.ga(Bootstrapper._BkPth$replace.GA_METHOD, Bootstrapper._BkPth$replace.GA_EVENT, Bootstrapper._BkPth$replace.GA_EXCEPTION_CATEGORY, Bootstrapper._BkPth$replace.GA_EXCEPTION_ACTION, JSON.stringify(customLabel));
};
"""



QUALIFICATION_CODE = """DL_OBJ = Bootstrapper._BkPth$replace

function requestCampagin() {
    try {
        if (CONDITION) {

            if (!DL_OBJ.CAMPAIGNREQUESTED) {
                renderer.getContent(DL_OBJ.VIRTUALPAGE).done(function () {
                    renderer.runVariantJs();
                });
                DL_OBJ.CAMPAIGNREQUESTED = true;
            }
        } else {
            DL_OBJ.EXCLUDE_REASON = 'excludeinelegible| Message';
        }

    } catch (e) {
        var msg = 'Exception occured in running checkIFBundlePresnet method',
            method = 'checkIFBundlePresnet'
        input = {
            "error_message": e.message,
            "error_name": e.name,
        };
        DL_OBJ.dataGapHandler(msg, method, input);
    }
}

// self-executable function which trigger the Abandon modal fire methad
(function runVariant() {
    var passChecks = true;
    try {

        if (window.$ && typeof (window.$) === "function" && window.ga && typeof (window.ga) === "function" && Bootstrapper && UA $condition) {
            requestCampagin();

            if (DL_OBJ.EXCLUDE_REASON) {
                window.ga(DL_OBJ.GA_METHOD, DL_OBJ.GA_EVENT, DL_OBJ.GA_CATEGORY, DL_OBJ.CAMPAIGN_NAME, DL_OBJ.EXCLUDE_REASON);
            }

        } else {
            passChecks = false;
        }

        /* if did not pass checks, then recall function to check again after a specified time period */
        if (!passChecks) {
            setTimeout(runVariant, 10);
        }
    } catch (e) {
        // statements
        var msg = "exception occur while rendering campaign script",
            method = 'runVariant',
            input = {
                "error_message": e.message,
                "error_name": e.name
            };
        DL_OBJ.dataGapHandler(msg, method, input);
    }
})();

"""

VARIANT_CODE = """<script>
   var DL_OBJ = Bootstrapper._BkPth$replace;
   
    function runVariant() {
        try {
                        
        } catch (e) {
            var msg = "Exception occur in running runVariant method",
                method = 'runVariant',
                input = {
                    "error_message": e.message,
                    "error_name": e.name
                };
            DL_OBJ.dataGapHandler(msg, method, input);
        }
    }
</script>
"""

ANALYTICS_CODE = """
var DL_OBJ = Bootstrapper._BkPth$replace;

(function runScript() {
    var passChecks = true;
    try {

        if (window.$ && typeof (window.$) === "function" && window.ga && typeof (window.ga) === "function" && Bootstrapper && UA) {
            enableAnalyticsTracking();
        } else {
            passChecks = false;
        }

        /* if did not pass checks, then recall function to check again after a specified time period */
        if (!passChecks) {
            setTimeout(runScript, 10);
        }
    } catch (e) {
        // statements
        var msg = "exception occur while rendering analytics script",
            method = 'runScript',
            input = {
                "error_message": e.message,
                "error_name": e.name
            };
        DL_OBJ.dataGapHandler(msg, method, input);
    }
})();

function enableAnalyticsTracking(){
    try{

    } catch(e){
        var msg = 'Exception occured in running enableAnalyticsTracking method',
            method= 'enableAnalyticsTracking',
            input = {
                "error_message":e.message,
                "error_name":e.name,
            };
        DL_OBJ.dataGapHandler(msg, method, input);
    }
}

"""