import fetch from 'node-fetch';


// -------------------------
// Response Handlers
// -------------------------


type ResponseCallback = (response) => any

export interface ResponseHandlers {
    [responseCode: number]: ResponseCallback,
    onError?: (err) => any
}




// -------------------------
// Server Client
//
// -------------------------

export class ServerClient {

    public baseUrl: string;

    constructor(baseUrl: string) {
        this.baseUrl = baseUrl;
    }

    /**
     * Send a GET request to given url.
     *
     */
    public async get(url: string, responseHandlers: ResponseHandlers={}, urlQuery?): Promise<any | undefined> {
        return ((fetch(this._buildUrl(url, urlQuery))
                .then(res => {
                    if (res.status in responseHandlers){
                        responseHandlers[res.status](res)
                    } else{
                        return res.json()
                    }

                })
                .catch(err => {
                    if (responseHandlers.onError){responseHandlers.onError(err)}

                })
        ));
    }

    /**
     * Send a POST request to given url.
     *
     */
    public async post(url: string, postData?: object, responseHandlers: ResponseHandlers={}): Promise<any | undefined> {
        let headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        };
        return ((fetch(this._buildUrl(url), {
                body: JSON.stringify(postData),
                method: 'POST',
                headers: headers
            })
                .then(res => {
                    if (res.status in responseHandlers){
                        responseHandlers[res.status](res)
                    } else {
                        return res.json()
                    }
                })
                .catch(err => {
                    if (responseHandlers.onError){responseHandlers.onError(err)}
                })
        ));
    }

    /**
     * Send a PATCH request to given url.
     *
     */
    public async patch(url: string, patchData?: object, responseHandlers: ResponseHandlers={}): Promise<any | undefined> {
        return ((fetch(this._buildUrl(url), {
                body: JSON.stringify(patchData),
                method: 'PATCH',
            })
                .then(res => {
                    if (res.status in responseHandlers){
                        responseHandlers[res.status](res)
                    } else {
                        return res.json()
                    }
                })
                .catch(err => {
                    if (responseHandlers.onError){responseHandlers.onError(err)}
                })
        ));
    }

    /**
     * Send a DELETE request to given url.
     *
     */
    public async delete(url: string, postData?: object, responseHandlers: ResponseHandlers={}): Promise<Response | undefined> {
        return ((fetch(this._buildUrl(url), {
                method: 'DELETE',
            })
                .then(res => {
                    if (res.status in responseHandlers){
                        responseHandlers[res.status](res)
                    } else {
                        return res
                    }
                })
                .catch(err => {
                    if (responseHandlers.onError){responseHandlers.onError(err)}
                })
        ));
    }

    private _buildUrl(url: string, urlQuery?): string {
        let fullUrl = this.baseUrl + url;
        if (urlQuery){
            fullUrl = fullUrl + '?' + urlQuery
        }
        return fullUrl
    }



}
