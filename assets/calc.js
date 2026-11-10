/* Hawaii "all-inclusive-style" trip cost estimator. Runs entirely in the browser; nothing is sent anywhere. */
(function () {
  var form = document.getElementById('calc');
  if (!form) return;
  var $ = function (id) { return document.getElementById(id); };
  var money = function (n) {
    return '$' + Math.round(n).toLocaleString('en-US');
  };
  var num = function (id) {
    var v = parseFloat($(id).value);
    return isFinite(v) && v > 0 ? v : 0;
  };

  $('food-style').addEventListener('change', function () {
    var v = this.value;
    if (v) { $('food').value = v; }
    update();
  });

  function update() {
    var nights = num('nights');
    var adults = num('adults');
    var kids = num('kids');
    var room = num('room');
    var fee = num('fee');
    var parking = num('parking');
    var tax = num('tax') / 100;
    var food = num('food');
    var fun = num('fun');
    var days = nights + 1;
    var people = adults + kids;

    var lodging = (room + fee) * nights;
    var taxes = lodging * tax;
    var park = parking * nights;
    // Kids are budgeted at 60% of the adult food figure.
    var meals = food * days * (adults + kids * 0.6);
    var activities = fun * people;
    var total = lodging + taxes + park + meals + activities;

    $('o-lodging').textContent = money(lodging);
    $('o-taxes').textContent = money(taxes);
    $('o-parking').textContent = money(park);
    $('o-meals').textContent = money(meals);
    $('o-fun').textContent = money(activities);
    $('o-total').textContent = money(total);
    $('o-pppd').textContent = people && days ? money(total / people / days) : '$0';
  }

  form.addEventListener('input', update);
  form.addEventListener('submit', function (e) { e.preventDefault(); update(); });
  update();
})();
