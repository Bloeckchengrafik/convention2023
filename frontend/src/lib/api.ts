export async function endpoint<T>(ep: string): Promise<T> {
    let res: Response;
    try {
        res = await fetch(`http://127.0.0.1:5000/${ep}`);
    } catch (err) {
        console.log("Meta API error: " + err);
        throw new Error(`Meta API error: ${err}`);
    }
    if (!res.ok) {
        console.log("API error: ", res.status, res.statusText);
        throw new Error(`API error: ${res.status}`);
    }
    return await res.json();
}