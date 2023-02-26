export async function fetchWithTimeout(resource, timeout) {
  let response;
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    await fetch(resource, {
      signal: controller.signal,
    }).then((service_res) => {
      response = service_res.json();
    });
  } catch (e) {
    return false;
  } finally {
    clearTimeout(timeoutId);
  }

  return response;
}
