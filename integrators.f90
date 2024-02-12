subroutine compute_forces_1D(F, phi_minus, phi_plus, N, x)
  implicit none
  integer :: i
  integer, intent(in) :: N
  real(8), intent(in):: phi_minus(0:N), phi_plus(0:N), x(0:N)
  real(8), intent(inout) :: F(0:N)

  F(0) = phi_plus(0)/((x(0)-x(1))*(x(0)-x(1)))

  do i=1,N-1
    F(i)=(phi_minus(i)/((x(i-1)-x(i))*(x(i-1)-x(i+1))))&
        +(phi_plus(i)/((x(i)-x(i+1))*(x(i-1)-x(i+1))))
  end do

  F(N) = (phi_minus(N)/((x(N-1)-x(N))*x(N-1)))&
         +phi_plus(N)/(x(N)*x(N-1))
end subroutine

subroutine compute_forces_2D(F, phi_minus, phi_plus, N, x)
  implicit none
  integer :: i
  integer, intent(in) :: N
  real(8), intent(in):: phi_minus(0:N), phi_plus(0:N), x(0:N)
  real(8), intent(inout) :: F(0:N)

  F(0) = phi_plus(0)/((x(0)-x(1))*(x(0)+x(1))*(x(0)-x(1)))

  do i=1,N-1
    F(i)=(phi_minus(i)/((x(i-1)+x(i))*(x(i-1)-x(i))*(x(i-1)-x(i+1))))&
        +(phi_plus(i)/((x(i+1)+x(i))*(x(i)-x(i+1))*(x(i-1)-x(i+1))))
  end do

  F(N) = (phi_minus(N)/((x(N-1)-x(N))*(x(N)+x(N-1))*x(N-1)))&
         +phi_plus(N)/(x(N)*x(N)*x(N-1))
end subroutine

subroutine Velocity_Verlet_steps(steps, v, x, phi_minus, phi_plus, N, dt, dimensions)
  implicit none
  integer :: steps, i, N, dimensions
  real(8) :: F(0:N), v(0:N), x(0:N), phi_minus(0:N), phi_plus(0:N), dt

  if ( dimensions==1 ) then
    call compute_forces_1D(F, phi_minus, phi_plus, N, x)
    v = v + F*0.5d0*dt
    do i=1,steps
      x = x + v*dt
      call compute_forces_1D(F, phi_minus, phi_plus, N, x)
      v = v + F*dt
    end do
  else if ( dimensions==2 ) then
    call compute_forces_2D(F, phi_minus, phi_plus, N, x)
    v = v + F*0.5d0*dt
    do i=1,steps
      x = x + v*dt
      call compute_forces_2D(F, phi_minus, phi_plus, N, x)
      v = v + F*dt
    end do
  end if




  v = v - F*0.5d0*dt

end subroutine

subroutine PEFRL_steps(steps, v, x, phi_minus, phi_plus, N, dt, dimensions)
  ! https://doi.org/10.1016/S0010-4655(02)00451-4
  implicit none
  integer :: i, N
  integer, intent(in):: steps, dimensions
  real(8), intent(inout) :: v(0:N), x(0:N)
  real(8), intent(in) :: phi_minus(0:N), phi_plus(0:N), dt
  real(8) :: F(0:N)
  real(8) :: xi = .1786178958448091d0,&
             la =-.2123418310626054d0,&
             ji =-.6626458266981849d-1

  x=x+v*xi*dt
  if ( dimensions==1 ) then
    do i=1,steps
      call compute_forces_1D(F, phi_minus, phi_plus, N, x)
      v=v+(0.5d0-la)*dt*F
      x=x+ji*dt*v
      call compute_forces_1D(F, phi_minus, phi_plus, N, x)
      v=v+la*dt*F
      x=x+(1.d0-2.d0*(ji+xi))*dt*v
      call compute_forces_1D(F, phi_minus, phi_plus, N, x)
      v=v+la*dt*F
      x=x+ji*dt*v
      call compute_forces_1D(F, phi_minus, phi_plus, N, x)
      v=v+F*(0.5d0-la)*dt
      x=x+2.d0*xi*v*dt
    end do
  else if ( dimensions==2 ) then
    do i=1,steps
      call compute_forces_2D(F, phi_minus, phi_plus, N, x)
      v=v+(0.5d0-la)*dt*F
      x=x+ji*dt*v
      call compute_forces_2D(F, phi_minus, phi_plus, N, x)
      v=v+la*dt*F
      x=x+(1.d0-2.d0*(ji+xi))*dt*v
      call compute_forces_2D(F, phi_minus, phi_plus, N, x)
      v=v+la*dt*F
      x=x+ji*dt*v
      call compute_forces_2D(F, phi_minus, phi_plus, N, x)
      v=v+F*(0.5d0-la)*dt
      x=x+2.d0*xi*v*dt
    end do
  end if

  x=x-v*xi*dt
end subroutine
