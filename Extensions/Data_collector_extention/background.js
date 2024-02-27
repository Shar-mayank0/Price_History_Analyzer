chrome.tabs.onUpdated.addListener((tabId, changeinfo, tab) =>{
    if(changeinfo.status == 'complete'){
        console.log('Tab updated');
        const p_url = tab.url;
        const amazonProductPage = /https:\/\/www.amazon.in\/.*\/dp\/.*/;
        const flipkartproductpage = /https:\/\/www.flipkart.com\/.*\/p\/.*/;
        if (tab.url && flipkartproductpage.test(p_url)){
            console.log('Flipkart product page detected', p_url);
            let params = new URLSearchParams(new URL(p_url).search);
            const pid = params.get('pid');
            if (pid === null) {
                console.log("'pid' parameter is not present in the URL");
            } else {
                console.log(`'pid' parameter value is: ${pid}`);
            }
            console.log('Flipkart product page detected');
            chrome.action.setPopup({ popup: 'popup.html' });
            const url_Data = {Product_ID: pid, Product_URL: p_url, Product_site: 'flipkart'};
            console.log(url_Data);
            console.log('Product ID:', pid);
            console.log('Product URL:', p_url);
            fetch(`http://localhost:3000/api/v1/ext/flipkartproducts/url`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(url_Data), // Convert url_Data to JSON
                })
                .then(response => response.text())
                .then(data => {
                    console.log('Success:', data);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        
        };
        if (tab.url && amazonProductPage.test(p_url)){
            console.log('Amazon product page detected', p_url);
            chrome.action.setPopup({popup: 'popup.html'});
            const productID = p_url.split('/dp/')[1].split(/[/?]+/)[0];
            const url_Data = {Product_ID: productID, Product_URL: p_url, Product_site: 'amazon'};
            console.log(url_Data);
            console.log('Product ID:', productID);
            console.log('Product URL:', p_url);
            fetch(`http://localhost:3000/api/v1/ext/amazonproducts/url`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(url_Data), // Convert url_Data to JSON
                })
                .then(response => response.text())
                .then(data => {
                    console.log('Success:', data);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    }
});
