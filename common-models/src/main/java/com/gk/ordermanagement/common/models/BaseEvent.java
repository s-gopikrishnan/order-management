package com.gk.ordermanagement.common.models;

import com.fasterxml.jackson.annotation.JsonSubTypes;
import com.fasterxml.jackson.annotation.JsonTypeInfo;

@JsonTypeInfo(use = JsonTypeInfo.Id.NAME, include = JsonTypeInfo.As.PROPERTY, property = "type")
@JsonSubTypes({
    @JsonSubTypes.Type(value = OrderPlacedEvent.class, name = "OrderPlacedEvent"),
    @JsonSubTypes.Type(value = InventoryReservedEvent.class, name = "InventoryReservedEvent"),
    @JsonSubTypes.Type(value = InventoryFailedEvent.class, name = "InventoryFailedEvent"),
    @JsonSubTypes.Type(value = CustomerValidatedEvent.class, name = "CustomerValidatedEvent"),
    @JsonSubTypes.Type(value = CustomerFailedEvent.class, name = "CustomerFailedEvent"),
    @JsonSubTypes.Type(value = PaymentProcessedEvent.class, name = "PaymentProcessedEvent")
})
public interface BaseEvent {
}
