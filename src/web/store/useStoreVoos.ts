
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

    const outboundTicketClass = ref<'economy' | 'premium'>('economy')
    const inboundTicketClass = ref<'economy' | 'premium'>('economy')

    const passenger = ref({
        firstName: '',
        lastName: '',
        document: '',
        birthDate: ''
    })
    const selectedSeats = ref<Record<string, string>>({}) // flightId -> seatCode

    const totalPrice = computed(() => {
        let total = 0
        if (outboundFlight.value) {
            total += outboundFlight.value.tickets?.[outboundTicketClass.value] || 0
        }
        if (inboundFlight.value) {
            total += inboundFlight.value.tickets?.[inboundTicketClass.value] || 0
        }
        return total
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

    function setOutboundTicketClass(cls: 'economy' | 'premium') {
        outboundTicketClass.value = cls
    }

    function setInboundTicketClass(cls: 'economy' | 'premium') {
        inboundTicketClass.value = cls
    }

    function updatePassenger(data: any) {
        passenger.value = { ...passenger.value, ...data }
    }

    function selectSeat(flightId: string, seatCode: string) {
        selectedSeats.value[flightId] = seatCode
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
        outboundTicketClass.value = 'economy'
        inboundTicketClass.value = 'economy'
        selectedSeats.value = {}
        passenger.value = { firstName: '', lastName: '', document: '', birthDate: '' }
    }

    return {
        outboundFlight,
        inboundFlight,
        selectionParams,
        outboundTicketClass,
        inboundTicketClass,
        passenger,
        selectedSeats,
        totalPrice,
        ticketsTotal: totalPrice, // Alias for now
        setOutboundFlight,
        setInboundFlight,
        setSelectionParams,
        setOutboundTicketClass,
        setInboundTicketClass,
        updatePassenger,
        selectSeat,
        clearSelection
    }
})
