export { itemButton };

/**
 * Add, remove and list buttons from a coma separated text input or
 * from a select box.
 */
function itemButton() {
  let publicAPI = {};

  /**
   * Adds a deletable button from either an input or select tag.
   * @param {string} items - single item or string of comma separated items.
   * @param {string} selectionsLoc - id of the location the item buttons will be placed.
   * @param {number} numSelections - Total number of items permitted.
   */
  publicAPI.add = (items, selectionsLoc, numSelections) => {
    //Get the current list of button items.
    let currentItems = publicAPI.list(selectionsLoc);

    // If no items exists in button location item counter equals numSelection
    // else subtract the length of he current items.
    let itemCounter = !currentItems
      ? numSelections
      : numSelections - currentItems.length;

    if (itemCounter < 1) return; // If zero then  max number of items has been met.

    // ****Validate*****
    // separate by coma (if it exists) then filter our blank items.
    items
      .split(",")
      .filter((item) => item.trim().length != 0)
      .forEach((item) => {
        if (itemCounter < 1) return;

        //Reduce string length to 30 characters.
        let itemShort = item.substring(0, 25);

        // ****Create ID and Values*****
        // Create ID
        let itemID = itemShort
          .trim()
          .replace(/\s+/g, "-") //Replace spaces with dashes.
          .replace(/[^0-9a-z-]/gi, "") //Remove anything that isn't alphanumeric.
          .toLowerCase();

        //If itemID starts with a number add teh letter "a" so it is a valid HTML ID.
        itemID = isNaN(itemID[0]) ? itemID : `a${itemID}`;

        //Create Item Value
        let itemVal = itemShort.replace(/[^0-9a-z ]/gi, ""); //Remove anything that isn't alphanumeric.

        //Check if ID exits in current lists.
        let alreadyExists = false;
        if (currentItems) {
          for (let i = 0; i < currentItems.length; i++) {
            if (currentItems[i].id === itemID) {
              return (alreadyExists = false);
            }
          }
        }
        if (alreadyExists) return;

        // ****Create button*****
        //Create new span
        let selectionSpan = document.createElement("span");
        selectionSpan.setAttribute("value", itemVal);
        selectionSpan.setAttribute("id", itemID);
        selectionSpan.setAttribute("class", "item-btn");

        selectionSpan.innerHTML = `${itemVal} <button type="button" id="${itemID}" class="item-x-btn">✖</button>`;

        let selectLoc = document.querySelector(`#${selectionsLoc}`);
        selectLoc.appendChild(selectionSpan);

        // ****Add event listener for new button attached to item.****
        let selectedSpan = selectLoc.querySelector(`#${itemID}`);

        //Add an event listener on the "x" button to remove the item if clicked.
        selectedSpan.querySelector("button").addEventListener("click", () => {
          selectedSpan.remove();
        });

        --itemCounter;
        currentItems = publicAPI.list(selectionsLoc);
      });
  };

  /**
   * Get all the items in a selected tag location or false if none exist.
   * @param {string} selectionsLoc id of the location the item buttons will be placed.
   * @return {object|boolean} object of all current item buttons in selected tag
   *                          containing {id: , val: }. If none then false.
   */
  publicAPI.list = (selectionsLoc) => {
    let items = document.getElementById(selectionsLoc).querySelectorAll("span");

    //If no items exists return false
    if (items.length == 0) {
      return false;
    }
    return Object.keys(items).map((item) => {
      return {
        id: items[item].id,
        val: (() => {
          let val = items[item].innerText;
          return val.substr(0, val.length - 2);
        })(),
      };
    });
  };

  return publicAPI;
}