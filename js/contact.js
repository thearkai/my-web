/* ==========================================================================
   js/contact.js — contact form validation and submission
   --------------------------------------------------------------------------
   HOW DELIVERY WORKS RIGHT NOW
   No form service is configured, so the form validates the input and then
   opens the visitor's email app with the message pre-filled. It never claims
   a message was "sent", because nothing was sent.

   TO CONNECT A REAL SERVICE (free tiers):
     1. Create a form at Formspree, Getform, Basin or Netlify Forms.
     2. Put its endpoint in FORM_ENDPOINT below, e.g.
        var FORM_ENDPOINT = "https://formspree.io/f/xxxxxxxx";
   The fetch-based delivery path is already written below and activates as
   soon as that constant is filled in.
   ========================================================================== */

(function () {
  "use strict";

  var FORM_ENDPOINT = "";                    // <-- paste your form endpoint here
  var OWNER_EMAIL = "actinsyson24@gmail.com";

  var form = document.querySelector("[data-contact-form]");
  if (!form) return;

  var statusEl = form.querySelector("[data-form-status]");
  var submitBtn = form.querySelector('button[type="submit"]');
  var submitLabel = submitBtn ? submitBtn.innerHTML : "";

  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  /* Validation rules per field name. Return "" when the value is fine. */
  var rules = {
    name: function (value) {
      if (!value) return "Please enter your name.";
      if (value.length < 2) return "That name looks a little short.";
      return "";
    },
    email: function (value) {
      if (!value) return "Please enter your email address.";
      if (!EMAIL_RE.test(value)) return "Please enter a valid email address.";
      return "";
    },
    subject: function (value) {
      if (!value) return "Please add a short subject.";
      if (value.length < 3) return "Please use at least 3 characters.";
      return "";
    },
    message: function (value) {
      if (!value) return "Please write a message.";
      if (value.length < 12) return "Please add a little more detail (12+ characters).";
      return "";
    }
  };

  /* ------------------------------------------------------------- helpers */
  function fieldOf(name) {
    return form.querySelector('[name="' + name + '"]');
  }

  function setError(name, message) {
    var input = fieldOf(name);
    if (!input) return;
    var wrapper = input.closest(".field");
    var errorEl = wrapper ? wrapper.querySelector(".field-error") : null;

    if (wrapper) wrapper.classList.toggle("has-error", Boolean(message));
    input.setAttribute("aria-invalid", message ? "true" : "false");
    if (errorEl) errorEl.textContent = message;
  }

  function validateField(name) {
    var input = fieldOf(name);
    if (!input || !rules[name]) return true;
    var message = rules[name](input.value.trim());
    setError(name, message);
    return !message;
  }

  function showStatus(message, type, iconId) {
    if (!statusEl) return;
    statusEl.className = "form-status is-visible is-" + type;
    statusEl.innerHTML =
      '<svg class="icon" aria-hidden="true"><use href="#i-' + iconId + '"></use></svg>' +
      "<span>" + message + "</span>";
  }

  function clearStatus() {
    if (!statusEl) return;
    statusEl.className = "form-status";
    statusEl.innerHTML = "";
  }

  function setLoading(isLoading) {
    if (!submitBtn) return;
    submitBtn.disabled = isLoading;
    submitBtn.innerHTML = isLoading
      ? '<span class="spinner" aria-hidden="true"></span> preparing…'
      : submitLabel;
  }

  /* ------------------------------------------------- live field feedback */
  Object.keys(rules).forEach(function (name) {
    var input = fieldOf(name);
    if (!input) return;

    input.addEventListener("blur", function () {
      validateField(name);
    });

    input.addEventListener("input", function () {
      var wrapper = input.closest(".field");
      if (wrapper && wrapper.classList.contains("has-error")) validateField(name);
    });
  });

  /* ----------------------------------------------------------- submission */
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    clearStatus();

    // Validate every field (map first — Array.every() would short-circuit)
    var results = Object.keys(rules).map(validateField);
    var allValid = results.every(Boolean);

    if (!allValid) {
      var firstInvalid = form.querySelector(".field.has-error input, .field.has-error textarea");
      if (firstInvalid) firstInvalid.focus();
      showStatus("Please fix the highlighted fields and try again.", "error", "alert");
      return;
    }

    var data = {
      name: fieldOf("name").value.trim(),
      email: fieldOf("email").value.trim(),
      subject: fieldOf("subject").value.trim(),
      message: fieldOf("message").value.trim()
    };

    setLoading(true);

    /* ---- Path A: a real form service is configured ---------------------- */
    if (FORM_ENDPOINT) {
      fetch(FORM_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(data)
      })
        .then(function (response) {
          if (!response.ok) throw new Error("Request failed");
          form.reset();
          showStatus(
            "Thanks, " + data.name + " — your message was sent. I'll reply to " +
            data.email + " as soon as I can.",
            "success",
            "check"
          );
        })
        .catch(function () {
          showStatus(
            "Something went wrong sending that. Please email me directly at " +
            OWNER_EMAIL + ".",
            "error",
            "alert"
          );
        })
        .then(function () {
          setLoading(false);
        });
      return;
    }

    /* ---- Path B: no service yet — hand off to the visitor's mail app ---- */
    var body =
      "Name: " + data.name + "\n" +
      "Email: " + data.email + "\n\n" +
      data.message + "\n";

    var mailto =
      "mailto:" + OWNER_EMAIL +
      "?subject=" + encodeURIComponent("[Portfolio] " + data.subject) +
      "&body=" + encodeURIComponent(body);

    // Small delay so the loading state is visible rather than a flicker
    window.setTimeout(function () {
      setLoading(false);

      window.location.href = mailto;

      showStatus(
        "This form isn't connected to a mail service yet, so your email app is opening with the message ready to send. " +
        'If nothing happened, email me directly at <a href="mailto:' + OWNER_EMAIL + '">' + OWNER_EMAIL + "</a>.",
        "info",
        "info"
      );
    }, 550);
  });
})();
