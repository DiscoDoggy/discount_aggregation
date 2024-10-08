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

class PaginationState
{

}

//basically state variables
let GLOBAL_state = 
{
    category: "",
    is_sorting_active: false,
    is_searching_active: false,
    is_filtering_active: false,
}

let GLOBAL_current_endpoint = "";
let GLOBAL_filter_json = "";
let GLOBAL_max_items_per_page = 50;

function update_offset(url, new_offset)
{
    const url_object = new URL(url);
    url_object.searchParams.set("offset", new_offset);
    const updated_url = url_object.toString();

    return updated_url;
}

async function get_item_data(url, request_body)
{
    console.log("entered get_item_data");
    let response_body = null;
    var response = null;

    try {
        if (request_body === null)
        {
            response = await fetch(url);
        }

        else
        {
            response = await fetch(url, request_body);
        }

        if(!response.ok) 
        {
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
    var color_set = new Set();
    var sizes_set = new Set();
    
    json_items.forEach((item) => {
        item.promo_price = item.promo_price.toFixed(2); // sets precision of values to two decimal points (should probably be done in preprocessing)
        var store_item = new StoreItem(item);
        append_location.appendChild(store_item);

        const color_append_location = store_item.getElementsByClassName("grid-colors");
        var item_color_list = item.colors;

        item_color_list.forEach((color) => {
            var color_element = new ColorBubble(color);
            color_append_location[0].appendChild(color_element);
            color_set.add(color);

        });

        var item_sizes = item.sizes;
        item_sizes.forEach((size) => {
            sizes_set.add(size);
        });

        
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

    var size_and_color_set = [sizes_set, color_set];
    return size_and_color_set;
}

function add_sizes_filters(unique_sizes)
{
    console.log("ENTERING ADD_SIZES_FILTERS");
    let append_location = document.getElementById("sizes-filter-container");
    let size_html = "";

    for (const size of unique_sizes)
    {
        let size_checkbox_container = document.createElement("div");

        let new_checkbox = document.createElement("input");
        new_checkbox.type = "checkbox";
        new_checkbox.className = "size-checkbox";
        new_checkbox.id = `${size}`;
        new_checkbox.checked = true;

        let new_checkbox_label = document.createElement("label");
        new_checkbox_label.htmlFor = `${size}`;
        new_checkbox_label.textContent = `${size}`;
        new_checkbox_label.className = "checkbox-grid-label";

        new_checkbox_label.appendChild(new_checkbox);
        size_checkbox_container.appendChild(new_checkbox_label);
        append_location.appendChild(size_checkbox_container);
    }

    // append_location.insertAdjacentHTML("afterend", size_html);

    
}

function add_color_filters(unique_colors)
{
    //takes in a set of colors
    console.log("ENTERING ADD_COLOR_FILTERS");
    let append_location = document.getElementById("color-filter-container");
    
    for(const color of unique_colors)
    {
        let checkbox_div = document.createElement("div");

        let checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.className = "color-checkbox";
        checkbox.checked = true;

        let checkbox_label = document.createElement("label");
        checkbox_label.innerText = `${color}`;

        checkbox_label.appendChild(checkbox);
        checkbox_div.appendChild(checkbox_label);
        append_location.appendChild(checkbox_div);
    }
}

function remove_items_from_page() {
    const item_container = document.getElementById("item-grid-container");
    const item_children = Array.from(item_container.children);
    for(let child of item_children) {
        // console.log(child.textContent);
        child.remove();
    } 
}

async function fetch_sorted_items(sort_param) {
    console.log("SORTING BUTTON CLICKED");
    var url = GLOBAL_current_endpoint;
    

    //lets make the assumption that sort_param will always be at the end of query parameters
    // ?limit=w&offset=x&search_query=y&sort_key=z
    let sort_query_exist_index = GLOBAL_current_endpoint.indexOf("&sort_key");
    if(sort_query_exist_index == -1)
    {
        GLOBAL_current_endpoint = GLOBAL_current_endpoint + `&sort_key=${sort_param}`
    } 
    else
    {
        
        GLOBAL_current_endpoint = GLOBAL_current_endpoint.substring(0, sort_query_exist_index);
        GLOBAL_current_endpoint = GLOBAL_current_endpoint + `&sort_key=${sort_param}`;
    }
    
    let sorted_items_json = null;

    if(GLOBAL_current_endpoint.includes("filter"))
    {
        sorted_items_json = await get_item_data(GLOBAL_current_endpoint, GLOBAL_filter_json); 
    }
    else
    {
        sorted_items_json = await get_item_data(GLOBAL_current_endpoint, null);
    }
    
    remove_items_from_page();
    write_items_to_page(sorted_items_json);
    if(sorted_json_items.length)
        {
            let total_items = sorted_items_json_items[0].num_total_items;
            create_pagination_element(total_items);

        }


}

function init_events()
{
    const sort_dropdown_children = document.getElementById("sort-dropdown-list");
    for (const child of sort_dropdown_children.children) {
        child.addEventListener("click", ()=> {
            fetch_sorted_items(child.getAttribute("id"));
        });
    }

    const min_price_input = document.getElementById("min-price-filter-input");
    const max_price_input = document.getElementById("max-price-filter-input");

    min_price_input.addEventListener("input", ()=> {
        price_validation(min_price_input, max_price_input);
        console.log("Enter addEventListener for price input");
    });

    max_price_input.addEventListener("input", ()=>{
        price_validation(min_price_input, max_price_input);
        console.log("entered event for changing max_price_input");
    });

    var any_size_checkbox = document.getElementById("any-size-checkbox");
    any_size_checkbox.addEventListener("click", ()=> {
        handle_any_checkbox(any_size_checkbox, "size-checkbox");
    });

    var size_checkboxes = document.getElementsByClassName("size-checkbox");

    for (let i = 0; i < size_checkboxes.length; i++)
    {
        size_checkboxes[i].addEventListener("click", ()=> {    
            handle_subcategory_checkbox_change(any_size_checkbox, "size-checkbox");
        });
    }

    var any_color_checkbox = document.getElementById("any-color-checkbox");
    var color_checkboxes = document.getElementsByClassName("color-checkbox");
    any_color_checkbox.addEventListener("click", ()=> {
        handle_any_checkbox(any_color_checkbox, "color-checkbox");
    });

    for(let i = 0; i < color_checkboxes.length; i++)
    {
        color_checkboxes[i].addEventListener("click", ()=>{
            handle_subcategory_checkbox_change(any_color_checkbox, "color-checkbox");
        });
    }

    var rating_checkboxes = document.getElementsByClassName("rating-checkbox");

    const submit_filter_button = document.getElementById("submit-filters-button");
    submit_filter_button.addEventListener("click", ()=> {
        handle_filtering(
            min_price_input.value,
            max_price_input.value,
            any_size_checkbox,
            size_checkboxes,
            any_color_checkbox,
            color_checkboxes,
            rating_checkboxes
        );
    });

    const default_filters_button = document.getElementById("default-filters-button");
    default_filters_button.addEventListener("click", async ()=>{
        var index = GLOBAL_current_endpoint.indexOf("/filter");
        if(index != -1)
        {
            GLOBAL_current_endpoint = GLOBAL_current_endpoint.substring(0, index);
            json_items = await get_item_data(GLOBAL_current_endpoint, null);
            remove_items_from_page();
            write_items_to_page(json_items);

            min_price_input.value = "";
            max_price_input.value = "";
            
            any_size_checkbox.checked = true;
            for(let i = 0; i < size_checkboxes.length; i++)
            {
                size_checkboxes[i].checked = true;
            }
    
            any_color_checkbox.checked = true;
            for(let i = 0; i < color_checkboxes.length; i++)
            {
                color_checkboxes[i].checked = true;
            }
    
            for(let i = 0; i < rating_checkboxes.length; i++)
            {
                rating_checkboxes[i].checked = true;
            }
        }
        else
        {
            alert("All default filters are currently active");
        }

    });

    var search_button = document.getElementById("search-button");
    var search_bar = document.getElementById("search-bar");

    search_button.addEventListener("click", async ()=>{
        var search_query = search_bar.value;
        var query_symb_index = GLOBAL_current_endpoint.indexOf("?");
        if (query_symb_index != -1) {
            GLOBAL_current_endpoint = GLOBAL_current_endpoint.substring(0,query_symb_index);
        }
    
        GLOBAL_current_endpoint =  `http://127.0.0.1:8000/items/search?limit=${GLOBAL_max_items_per_page}&offset=0` 
        + `&search_query=${search_query}`;

        var json_items = await get_item_data(GLOBAL_current_endpoint, null);
        remove_items_from_page();
        write_items_to_page(json_items);
        if(json_items.length)
        {
            let total_items = json_items[0].num_total_items;
            create_pagination_element(total_items);

        }
        


    });
}

function handle_any_checkbox(any_checkbox_element, target_checkboxes_classname)
{
    var target_checkboxes = document.getElementsByClassName(target_checkboxes_classname);

    if (any_checkbox_element.checked)
    {
        for(let i = 0; i < target_checkboxes.length; i++)
        {
            target_checkboxes[i].checked = true;
        }
    }
    else
    {
        for(let i = 0; i < target_checkboxes.length; i++)
        {
            target_checkboxes[i].checked = false;
        }
    }
}

function handle_subcategory_checkbox_change(any_checkbox_element, target_checkboxes_class_name)
{
    var target_checkboxes = document.getElementsByClassName(target_checkboxes_class_name);
    var are_all_sizes_checked = true;
    for (let i = 0; i < target_checkboxes.length; i++)
    {
        if(!target_checkboxes[i].checked)
        {
            are_all_sizes_checked = false;
            any_checkbox_element.checked = false;
        }
    }

    if(are_all_sizes_checked)
    {
        any_checkbox_element.checked = true;
    }

}

function price_validation(min_price_element, max_price_element)
{
    var min_price = min_price_element.value;
    var max_price = max_price_element.value;

    console.log("enter price validation");
    if (min_price === "")
    {
        min_price_element.value = "";
        min_price = 0;
    }

    if(max_price === "")
    {
        max_price_element.value = "";
        max_price = 0;
    }

    min_price = Number(min_price);
    max_price = Number(max_price);
    if(max_price != 0 && min_price != 0 && min_price > max_price)
    {
        window.alert("Min price cannot be larger than max price!");
    }

    else if (min_price != 0 && max_price != 0 && max_price < min_price)
    {
        window.alert("Max price cannot be larger than min price!");
    }

}

async function handle_filtering (
    min_price, 
    max_price,
    any_size_checkbox,
    size_checkboxes,
    any_color_checkbox,
    color_checkboxes,
    rating_checkboxes
) {

    if (min_price === "")
    {
        min_price = 0;
    }

    if(max_price === "")
    {
        max_price = 0;
    }

    var sizes = [];
    console.log(`any size checkbox checked status: ${any_size_checkbox.checked}`);
    if(!any_size_checkbox.checked)
    {
        for(let i = 0; i < size_checkboxes.length; i++)
        {
            if(size_checkboxes[i].checked)
                sizes.push(size_checkboxes[i].id);
        }
    }

    var colors = [];
    if(!any_color_checkbox.checked)
    {
        colors = color_checkboxes;
    }

    var ratings = [];
    for(let i = 0; i < rating_checkboxes.length; i++)
    {
        if(rating_checkboxes[i].checked)
        {
            ratings.push(i);
        }
    }

    GLOBAL_filter_json = {
        method:"POST",
        body: JSON.stringify({
            min_price: min_price,
            max_price: max_price,
            sizes: sizes,
            colors: colors,
            ratings
        }),
        headers: {
            "Content-Type": "application/json",
        }
    }

    let query_symb_index = GLOBAL_current_endpoint.indexOf("/filter");

    if(query_symb_index != -1)
    {
        GLOBAL_current_endpoint = GLOBAL_current_endpoint.substring(0,query_symb_index);
    }

    else if (GLOBAL_current_endpoint.indexOf("?") != -1)
    {
        GLOBAL_current_endpoint = GLOBAL_current_endpoint.substring(0,GLOBAL_current_endpoint.indexOf("?"));
    }

    GLOBAL_current_endpoint = GLOBAL_current_endpoint + `/filter?limit=${GLOBAL_max_items_per_page}&offset=0`;
    console.log(`Current endpoint: ${GLOBAL_current_endpoint}`)

    json_items = await get_item_data(GLOBAL_current_endpoint, GLOBAL_filter_json);
    remove_items_from_page();
    write_items_to_page(json_items);
    if(json_items.length)
    {
            let total_items = json_items[0].num_total_items;
            create_pagination_element(total_items);
    }

   
}

//this needs to happen when a category, search, filter, or sort happens
function create_pagination_element(max_total_items)
{

    console.log(`max_total items: ${max_total_items}`);

    let pagination_list = document.getElementsByClassName("pagination");
    pagination_list = pagination_list[0];

    console.log(pagination_list);

    let pagination_children = pagination_list.children;
    console.log(`Paginatoin children ${pagination_children.length} `);

    if(pagination_children.length)
    {
        pagination_list.replaceChildren();
    }

    num_pages = Math.ceil(max_total_items / GLOBAL_max_items_per_page);
    console.log(`num pages: ${num_pages}`);
    for(let i = 0; i < num_pages; i++)
    {
        let page_item = document.createElement("li");
        page_item.className = "page-item";

        let page_link = document.createElement("a");
        page_link.textContent = i + 1;
        page_link.className = "page-link";

        page_link.addEventListener("click", async ()=> {
            GLOBAL_current_endpoint = update_offset(GLOBAL_current_endpoint, new_offset= i * GLOBAL_max_items_per_page)
            
            let json_items = null;
            if(GLOBAL_current_endpoint.includes("/filter"))
            {
                console.log("enters filtering endpoint");
                json_items = await get_item_data(GLOBAL_current_endpoint, GLOBAL_filter_json);
            }

            else
            {
                json_items = await get_item_data(GLOBAL_current_endpoint, null);
            }
            
            scroll(0,0);   
            remove_items_from_page();
            write_items_to_page(json_items);
                         
        });

        page_item.appendChild(page_link);
        pagination_list.appendChild(page_item);   
    }

}


async function main(api_url) 
{
    GLOBAL_current_endpoint = api_url;
    console.log(`Current endpoint: ${GLOBAL_current_endpoint}`)
    json_items = await get_item_data(GLOBAL_current_endpoint, null);
    
    var size_and_color_set = write_items_to_page(json_items);
    let total_items = json_items[0].num_total_items;
    add_sizes_filters(size_and_color_set[0]);
    add_color_filters(size_and_color_set[1]);

    init_events();
    create_pagination_element(total_items);

}

// export {create_pagination_element};

