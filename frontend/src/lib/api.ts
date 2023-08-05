export async function endpoint<T>(ep: string): Promise<T> {
    let res: Response;
    try {
        res = await fetch(`http://127.0.0.1:5000/${ep}`);
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
    } catch (err: any) {
        // no network error reporting
        if (err.name !== "TypeError") {
            console.log("Meta API error: " + err);
        }
        throw new Error(`Meta API error: ${err}`);
    }
    if (!res.ok) {
        console.log("API error: ", res.status, res.statusText);
        throw new Error(`API error: ${res.status}`);
    }
    return await res.json();
}

export function emptyPromise<T>(): Promise<T> {
    // eslint-disable-next-line @typescript-eslint/no-empty-function
    return new Promise<T>(() => {
    })
}