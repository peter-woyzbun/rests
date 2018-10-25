import fetch from 'node-fetch';


// -------------------------
// Response Handlers
// -------------------------


type ResponseCallback = (response) => void

export interface ResponseHandlers {
    [responseCode: number]: ResponseCallback,
    onError?: (err) => any
}

type RequestType = 'GET' | 'POST' | 'PATCH' | 'DELETE'


// -------------------------
// Server Client
//
// -------------------------

export class ServerClient {

    public baseUrl: string;
    public headerMiddleware: (header: object) => object;

    constructor(baseUrl: string) {
        this.baseUrl = baseUrl;
        this.headerMiddleware = (header) => header

    }

    private _requestOptions(requestType: RequestType, headers?: object, body?: any | undefined): object{
        if (!headers){
            headers = {}
        }
        let requestOptions = {
            method: requestType,
        };
        if (body){requestOptions['body'] = body}
        requestOptions['headers'] = this.headerMiddleware(headers);
        return requestOptions
    }

    /**
     * Send a GET request to given url.
     *
     */
    public async get(url: string, responseHandlers: ResponseHandlers={}, urlQuery?): Promise<any | undefined> {
        return ((fetch(this._buildUrl(url, urlQuery), this._requestOptions('GET'))
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
        return ((fetch(this._buildUrl(url), this._requestOptions('POST', headers, JSON.stringify(postData)))
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
        return ((fetch(this._buildUrl(url),
                this._requestOptions('PATCH', {}, JSON.stringify(patchData)))
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
        return ((fetch(this._buildUrl(url), this._requestOptions('DELETE'))
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
