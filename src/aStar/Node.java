package aStar;

import java.util.Collection;

public interface Node<N>{
	
	public boolean equals(Object n);
	public Collection<N> getChildren();
	public double getDistFromParent();
	
}
