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
                <img class="item-card-image" src = ${this.json_item.image_links[0]}>
            </div>
            <div class = "grid-item-name">${this.json_item.name}</div>
            <div class = "grid-item-gender">${this.json_item.gender}</div>
            <div class="grid-color-sizes-container">
                <div class="grid-colors">
                    ${this.json_item.colors}
                </div>
                <div class="grid-sizes">
                ${this.json_item.sizes}
                </div>
            </div>
            <div class="grid-item-price">$${this.json_item.promo_price}</div>
            <div class="grid-item-rating">⭐${this.json_item.rating} (${this.json_item.num_ratings})</div>
            <div class="grid-item-store-name">${this.json_item.site_name}</div>
        </div>
        `
    }
}

customElements.define("store-item", StoreItem);

async function get_item_data(url)
{
    console.log("entered get_item_data");
    let response_body = null;
    try {
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
    const append_location = document.getElementById("item-grid-container");
    json_items.forEach((item) =>{
        item.promo_price = item.promo_price.toFixed(2);
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