console.log('Script loaded'); // Add this line to check if the script is being loaded
document.addEventListener('DOMContentLoaded', function () {
console.log('DOMContentLoaded event triggered'); // Add this line to check if theDOMContentLoaded event is triggered
const addToCartButtons = document.querySelectorAll('.addToCart');
const viewCartButton = document.querySelector('.cart-container .btn-success');
const cart = {};
addToCartButtons.forEach(button => {
button.addEventListener('click', function () {
const bookName = this.getAttribute('data-book');
if (cart[bookName]) {
cart[bookName]++;
} else {
cart[bookName] = 1;
}
console.log('Cart Updated:', cart); // Log the updated cart
updateCartCount();
});
});
viewCartButton.addEventListener('click', function () {
console.log('View Cart Clicked');
alert('Cart Contents:\n' + JSON.stringify(cart, null, 2));
});
function updateCartCount() {
// Update the cart count display (you can customize this part based on your UI)
console.log('Updating Cart Count:', cart);
viewCartButton.innerHTML = `View Cart (${Object.values(cart).reduce((acc, val) => acc + val,
0)})`;
}
});