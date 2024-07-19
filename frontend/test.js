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
            <div class="grid-item-content>
                <div class="grid-item-store-name">${this.json_item.site_name}</div>
                <div class="grid-item-photo">
                    <img class="item-card-image" src = ${this.json_item.image_links[0]}>
                </div>
                <div class = "grid-item-name">${this.json_item.name}</div>
                <div class = "grid-item-gender">${this.json_item.gender}</div>
                <div class="grid-colors"></div>
                <div class="grid-sizes"></div>
                <div class="grid-item-price">$${this.json_item.promo_price}</div>
                <div class="grid-item-rating">⭐${this.json_item.rating} (${this.json_item.num_ratings})</div>
            </div>    
        </div>
        `
    }
}

class ColorBubble extends HTMLElement
{
    //for now this will be a string?? be good if we had a color code later like a #fc264 as example
    constructor(item_color)
    {
        super();
        this.item_color = item_color;
    }
    
    connectedCallback()
    {
        this.innerHTML = 
        `
        <div class="color-bubble-container">
            <label class="color-option">
                <input type="checkbox" name="color" value="red">
                <span class="color-bubble" style="background-color: ${this.item_color};"></span>
            </label>
        </div>
        `;

    }

}

customElements.define("store-item", StoreItem);
customElements.define("color-bubble", ColorBubble);
let GLOBAL_current_endpoint = "";

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
    
    json_items.forEach((item) => {
        item.promo_price = item.promo_price.toFixed(2); // sets precision of values to two decimal points (should probably be done in preprocessing)
        var store_item = new StoreItem(item);
        append_location.appendChild(store_item);

        const color_append_location = store_item.getElementsByClassName("grid-colors");
        var item_color_list = item.colors;

        item_color_list.forEach((color) => {
            var color_element = new ColorBubble(color);
            color_append_location[0].appendChild(color_element);

        });

        let item_sizes = item.sizes;
        let sizing_text = "";
        if (item_sizes.length == 0)
        {
            sizing_text = "No sizing available";
        }

        else if (item_sizes.length == 1)
        {
            sizing_text = item_sizes[0];
        }

        else
        {
            sizing_text = `${item_sizes[0]} - ${item_sizes[item_sizes.length - 1]}`;
        }

        let item_size_div = store_item.getElementsByClassName("grid-sizes")[0];
        item_size_div.textContent = sizing_text;

    });

}

function remove_items_from_page() {
    const item_container = document.getElementById("item-grid-container");
    const item_children = Array.from(item_container.children);
    for(let child of item_children) {
        // console.log(child.textContent);
        child.remove();
    } 
}


function handle_filtering() {
    //we want to get every box that is checked and create some sort of either json body
    //for a request or we can do this with all query parameters and rely on the backend to
    //parse out the restrictions
    console.log("Helklafl");
}

async function fetch_sorted_items(sort_param) {
    console.log("SORTING BUTTON CLICKED");
    var url = GLOBAL_current_endpoint;
    query_symb_index = url.indexOf("?");
    
    if (query_symb_index != -1) {
        url = url.substring(0,query_symb_index);
    }

    url = url + `?sort_key=${sort_param}`;
    console.log(`URL: ${url}`);
    GLOBAL_current_endpoint = url;
    
    sorted_items_json = await get_item_data(url);
    write_items_to_page(sorted_items_json);

}

function init_events()
{
    // const sort_button = document.getElementById("sort-button");
    // sort_button.addEventListener("click", handle_sort_button);

    const sort_dropdown_children = document.getElementById("sort-dropdown-list");
    for (const child of sort_dropdown_children.children) {
        child.addEventListener("click", ()=> {
            remove_items_from_page();
            fetch_sorted_items(child.getAttribute("id"));
        });
    }
    
    const submit_filter_button = document.getElementById("submit-filter-button");
    submit_filter_button.addEventListener("click", handle_filtering);
}

// window.onclick = (event) => {
//     var sort_drop_down_container = document.getElementById("sort-dropdown-content-container");

//     if (!event.target.matches("#sort-button") && !event.target.matches("#sort-dropdown-content-container") && !event.target.matches("#sort-dropdown-list")) {
//         console.log("Turning back to None");
//         sort_drop_down_container.style.display = "none";
//     }
// }

async function main() 
{
    var url = "http://127.0.0.1:8000/items/men";
    GLOBAL_current_endpoint = url;
    json_items = await get_item_data(url);
    write_items_to_page(json_items);
    
}


 //can be done async at same time as fetches, no overlap
console.log("hello world");
main();
init_events();


