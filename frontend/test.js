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


(function(){
"use strict";




async function get_item_data(url)
{
    try
    {
        const response = await fetch(url);
        if(!response.ok)
        {
            throw new Error(`Error. Response status: ${response.status}`);
        }
        var response_body = await response.json();
        console.log(response_body);
    }
    catch (error)
    {
        console.error("Fetch failure:", error);
    }

    return response_body;
}

function write_items_to_page(json_items)
{
    const append_location = document.getElementsByClassName("item-grid-container");
    json_items.forEach((item) => {
        store_item = StoreItem(item);
        append_location.appendChild(store_item);
    });

}

var json_items = get_item_data("http://127.0.0.1:8000/items/men/");
// write_items_to_page(json_items)




// url = "http://127.0.0.1:8000/items/men"

// fetch (url, {
//     method: "GET"
// }).then((response) => response.json())
// .then((json) => console.log(json));



})();

