document.addEventListener("DOMContentLoaded", function() {
  const specSelectors = [
    'select[name="especialidad"]',
    '#especialidad',
    'select[data-field="especialidad"]'
  ];
  const docSelectors = [
    'select[name="medico"]',
    '#medico',
    'select[data-field="medico"]'
  ];

  function pick(selList) {
    for (const s of selList) {
      const el = document.querySelector(s);
      if (el) return el;
    }
    return null;
  }

  const specEl = pick(specSelectors);
  const docEl  = pick(docSelectors);
  if (!specEl && !docEl) return; // no hay campos, no hacemos nada

  fetch("/v1/specialties/")
    .then(r=>r.json())
    .then(data => {
      if (specEl) {
        specEl.innerHTML = '<option value="">Seleccione especialidad</option>' +
          data.map(s=>`<option value="${s.slug}" data-id="${s.id}">${s.name}</option>`).join("");
      }
      // Cargar doctores según especialidad seleccionada
      function loadDoctorsBySlug(slug) {
        let url = "/v1/doctors/";
        if (slug) url += "?specialty_slug=" + encodeURIComponent(slug);
        fetch(url).then(r=>r.json()).then(list => {
          if (docEl) {
            docEl.innerHTML = '<option value="">Seleccione médico</option>' +
              list.map(d=>`<option value="${d.name}" data-id="${d.id}">${d.name}</option>`).join("");
          }
        }).catch(console.error);
      }
      if (specEl) {
        specEl.addEventListener("change", () => loadDoctorsBySlug(specEl.value));
        // carga inicial si hay valor por query (?specialty=slug)
        const u = new URL(window.location.href);
        const qSlug = u.searchParams.get("specialty");
        if (qSlug) {
          const opt = Array.from(specEl.options).find(o=>o.value===qSlug);
          if (opt) { specEl.value = qSlug; }
          loadDoctorsBySlug(qSlug);
        } else {
          loadDoctorsBySlug("");
        }
      } else {
        // Sin especialidad, cargamos todos los médicos
        loadDoctorsBySlug("");
      }
    }).catch(console.error);
});
