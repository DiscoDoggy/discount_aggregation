class StoreItem extends HTMLElement
{
    constructor(json_item)
    {
        super();
        this.json_item = json_item
    }

    connectedCallback()
    {
        this.innerHTML = 
        `
        <div class="grid-item">
            <div class="grid-item-photo">
                <img src = ${this.json_item.image_links[0]}>
            </div>
            <div class = "grid-item-name">${this.json_item.name}</div>
            <div class = "grid-item-gender">${this.json_item.gender}</div>
            <div class="grid-color-sizes-container">
                <div class="grid-colors">
                    red, blue, green
                </div>
                <div class="grid-sizes">
                    S, M, L
                </div>
            </div>
            <div class="grid-item-price">$29.90</div>
            <div class="grid-item-rating">⭐5.0 (51)</div>
            <div class="grid-item-store-name">Uniqlo</div>
        </div>
        `
    }
}

customElements.define("store-item", StoreItem);

async function get_item_data(url)
{
    console.log("entered get_item_data");
    let response_body = null;
    try{
        const response = await fetch(url);
        if(!response.ok) {
            throw new Error("Network response was not okay..." + response.status);
        }
        console.log("Response received:", response);
        response_body = await response.json();

        console.log("Parsed JSON:", response_body);
    }
    catch(error)
    {
        console.error("Fetch failure:", error);
    }
    console.log("Parsed json before function return:", response_body);
    return response_body;

}

function write_items_to_page(json_items)
{
    var append_location = document.getElementById("item-grid-container");
    console.log(append_location);
    json_items.forEach((item) =>{
        console.log(item.name);
        var store_item = new StoreItem(item);
        append_location.appendChild(store_item);
    });

}

async function main() 
{
    var url = "http://127.0.0.1:8000/items/men";
    json_items = await get_item_data(url);
    write_items_to_page(json_items);
}

main();


// const url = "http://127.0.0.1:8000/items/men"

// fetch (url, {
//     method: "GET"
// }).then((response) => response.json())
// .then((json) => console.log(json));



