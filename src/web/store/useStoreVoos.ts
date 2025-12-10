
import { defineStore } from 'pinia'

export const useStoreVoos = defineStore('voos', () => {
    const outboundFlight = ref<any>(null)
    const inboundFlight = ref<any>(null)
    const selectionParams = ref({
        origin_city: '',
        destination_city: '',
        departure_date: '',
        return_date: '',
        selected_class: ''
    })

    function setOutboundFlight(flight: any) {
        outboundFlight.value = flight
    }

    function setInboundFlight(flight: any) {
        inboundFlight.value = flight
    }

    function setSelectionParams(params: any) {
        selectionParams.value = { ...params }
    }

    function clearSelection() {
        outboundFlight.value = null
        inboundFlight.value = null
        selectionParams.value = {
            origin_city: '',
            destination_city: '',
            departure_date: '',
            return_date: '',
            selected_class: ''
        }
    }

    return {
        outboundFlight,
        inboundFlight,
        selectionParams,
        setOutboundFlight,
        setInboundFlight,
        setSelectionParams,
        clearSelection
    }
})
