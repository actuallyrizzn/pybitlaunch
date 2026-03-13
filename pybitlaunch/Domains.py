"""
BitLaunch DNS / domain records API.
See https://developers.bitlaunch.io/reference/list-records and Record Object.
"""
from .BaseAPI import BaseAPI, GET, POST, PUT, DELETE


class Record(object):
    """DNS record for a domain. Fields per BitLaunch API Record Object."""
    def __init__(self, hostname=None, type=None, value=None, ttl=None,
                 priority=None, weight=None, port=None, caaflag=None, caatype=None,
                 id=None, uid=None):
        self.id = id
        self.uid = uid
        self.hostname = hostname   # subdomain e.g. "@" or "app"
        self.type = type          # A, CNAME, MX, TXT, SRV, CAA, PTR
        self.value = value
        self.ttl = ttl            # time to live in seconds
        self.priority = priority  # lower = higher priority
        self.weight = weight      # for load balancing
        self.port = port          # for SRV
        self.caaflag = caaflag    # CAA criticality (0 or 128)
        self.caatype = caatype    # CAA certificate type


class DomainsService(BaseAPI):
    """DNS record operations: list, create, show, update, delete."""

    def __init__(self, *args, **kwargs):
        super(DomainsService, self).__init__(*args, **kwargs)

    def List(self, domain):
        """List all DNS records for a domain. GET /domains/{domain}/records"""
        if not domain or str(domain).strip() == "":
            return None, "No domain was provided"
        url = "domains/{}/records".format(str(domain).strip())
        data = self.getData(url)
        if data is not None and isinstance(data, dict) and "message" in data:
            return None, data["message"]
        return data, None

    def Show(self, domain, record_id):
        """Get a single DNS record by id. GET /domains/{domain}/records/{id}"""
        if not domain or str(domain).strip() == "":
            return None, "No domain was provided"
        if not record_id and record_id != 0:
            return None, "No record id was provided"
        url = "domains/{}/records/{}".format(str(domain).strip(), record_id)
        try:
            data = self.getData(url)
        except Exception as e:
            return None, str(e)
        if data is not None and isinstance(data, dict) and "message" in data:
            return None, data["message"]
        return data, None

    def Create(self, domain, record):
        """Create a DNS record. POST /domains/{domain}/records"""
        if not domain or str(domain).strip() == "":
            return None, "No domain was provided"
        if record is None:
            return None, "No record was provided"
        if getattr(record, "hostname", None) is None and getattr(record, "type", None) is None:
            return None, "Record must have hostname and type"
        if getattr(record, "value", None) is None or str(record.value).strip() == "":
            return None, "Record must have value"
        payload = {}
        for attr in ("hostname", "type", "value", "ttl", "priority", "weight", "port", "caaflag", "caatype"):
            v = getattr(record, attr, None)
            if v is not None:
                payload[attr] = v
        url = "domains/{}/records".format(str(domain).strip())
        data = self.getData(url, type=POST, params=payload)
        if data is not None and isinstance(data, dict) and "message" in data:
            return None, data["message"]
        return data, None

    def Update(self, domain, record_id, record):
        """Update a DNS record. PUT /domains/{domain}/records/{id}"""
        if not domain or str(domain).strip() == "":
            return None, "No domain was provided"
        if not record_id and record_id != 0:
            return None, "No record id was provided"
        if record is None:
            return None, "No record was provided"
        payload = {}
        for attr in ("hostname", "type", "value", "ttl", "priority", "weight", "port", "caaflag", "caatype"):
            v = getattr(record, attr, None)
            if v is not None:
                payload[attr] = v
        url = "domains/{}/records/{}".format(str(domain).strip(), record_id)
        data = self.getData(url, type=PUT, params=payload)
        if data is not None and isinstance(data, dict) and "message" in data:
            return None, data["message"]
        return data, None

    def Delete(self, domain, record_id):
        """Delete a DNS record. DELETE /domains/{domain}/records/{id}"""
        if not domain or str(domain).strip() == "":
            return "No domain was provided"
        if not record_id and record_id != 0:
            return "No record id was provided"
        url = "domains/{}/records/{}".format(str(domain).strip(), record_id)
        try:
            data = self.getData(url, type=DELETE)
        except Exception as e:
            return str(e)
        if data is not None and isinstance(data, dict) and "message" in data:
            return data["message"]
        return None
