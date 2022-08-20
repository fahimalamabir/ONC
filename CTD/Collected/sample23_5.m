close all; clearvars

%load dataset
load('./data/dataset_anl_137E.mat')
P        =nanmean(data.P,3);
S_mean   =nanmean(data.S,3);
T_mean   =nanmean(data.T,3);
S_mean   =nanmean(data.S,3);
PT_mean  =nanmean(data.PT,3);
PV_mean  =nanmean(data.PV,3);

%load climate index dataset
Cli =importdata('./misc_data/Index.xls');

for ii=1:1001 %down to 1000 dbar
for jj=1:size(data.S,2) 

    %Correlation Analysis between various climate indices 
    Lag      =3; %Lag year
    q        =data.mon==1 ; %winter
    yr       =data.yr(q);
    q_Cli    =Cli.data(:,1)>=min(yr) - Lag & Cli.data(:,1)<=max(yr) - Lag;
    PDO      =Cli.data(q_Cli,3);    

    %For potential temperature
    S_tmp =squeeze(data.S(ii,jj,q)); %potential temperature at ii-th layer and jj-th station
    [R,p]  =corrcoef([S_tmp,PDO]);
    S_PDO_R(ii,jj) =R(1,2); %Correlation coefficient
    S_PDO_p(ii,jj) =p(1,2); %p-value
    
end
end

%plot sectional distribution of correlation between salinity and PDO
figure('Position',[0,0,1200,800])
contourf(data.lat,[0:1000],S_PDO_R,20,'edgecolor','none');
xlabel('Latitude [deg N]')
ylabel('Pressure [dbar]')
set(gca,'ylim',[0,1000],'xdir','reverse','Fontsize',20)
colormap(redblue); 
cl=colorbar; 
ylabel(cl,'Corr Coeff between S and PDO-3yr lag')
caxis([-0.5,0.5]); 
axis ij; 
hold on
title('Contour: mean salinity')

%Contour line for showing p-value <0.05
contour(data.lat,[0:1000],S_PDO_p,[0, 0.05],'y-','linewidth',3)

%Show STMW, NPTW, and NPIW (Oka et al. 2018)
lat_all=repmat(data.lat,size(data.P,1),1);
q_STMW =PV_mean <2.5 *10^-10 & PT_mean>=16 & PT_mean<=19.5 & lat_all>7; %Suga et al. 1989 (PV: 2.0 -> 2.5 & lat>7)
q_NPTW =S_mean  >34.9        & lat_all>7; %Suga et al. 2000
q_NPIW =S_mean  <34.2        & P >200; %Shuto 1996

plot(lat_all(q_STMW),P(q_STMW),'g.')
plot(lat_all(q_NPTW),P(q_NPTW),'w.')
plot(lat_all(q_NPIW),P(q_NPIW),'k.')
title('Green: STMW, White: NPTW, Black: NPIW')

%Mean Salinity contour
[C,h] =contour(data.lat,[0:2030],S_mean(:,:,1),'k-');
set(h,'LevelStep',0.1,'ShowText','on','LineWidth',1,...
    'TextStep',get(h,'LevelStep')*2)
clabel(C,h,'Fontsize',16,'LabelSpacing',800);
set(gca,'xdir','reverse')

%Save figure
saveas(gcf,'sample23_5','jpg')

