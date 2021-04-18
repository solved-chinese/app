const Constant = {
    /**
     * Request time out in ms.
     */
    REQUEST_TIMEOUT: 5000,

    /**
     * Root element id.
     */
    ROOT_ELEMENT_ID: 'react-app',

    /**
     * Root element id.
     */
    HEADER_ELEMENT_ID: 'navbar-bg',
    ENV: (window.location.hostname == 'solvedchinese.org'? 'master' :
        window.location.hostname == 'dev.solvedchinese.org'? 'development' : null)
};

export default Constant;
