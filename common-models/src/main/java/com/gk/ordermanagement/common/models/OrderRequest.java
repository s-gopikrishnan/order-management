package com.gk.ordermanagement.common.models;

import java.time.LocalDateTime;
import java.util.List;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class OrderRequest {

	private String orderId;
	private List<String> productIds;
	private String customerId;
	private double totalAmount;
    private LocalDateTime placedTime;
    private LocalDateTime confirmedTime;
	
}
